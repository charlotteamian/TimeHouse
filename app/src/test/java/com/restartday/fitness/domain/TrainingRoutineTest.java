package com.restartday.fitness.domain;

import java.util.*;

public final class TrainingRoutineTest {
    static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
    static Exercise find(List<Exercise> pool, String id) {
        return pool.stream().filter(e -> e.id().equals(id)).findFirst().orElseThrow();
    }
    public static void main(String[] args) {
        Prescription optionalEffort = Prescription.hold(1, 20, "", 30, false);
        check(optionalEffort.holdSeconds() == 20 && optionalEffort.workSecondsPerSet() == 20, "Blank RPE must preserve the user's 20-second timer");
        check(!optionalEffort.compactLabel().contains("RPE"), "Blank RPE should not leave an empty label");
        check(new Prescription(1, "20", "7.5", 30).rpe().equals("7.5"), "Custom RPE is descriptive and may be decimal");
        List<Exercise> seeds = SeedExercises.defaultExercises();
        Exercise importedCurl = new Exercise.Builder("imported_curl", "Imported curl").regions("手臂").patterns("拉").build();
        check(!TrainingSelection.sameRole(importedCurl, find(seeds,"exercise_trx_row")), "Broad imported arm tags must not replace back compounds");
        RecommendationInput equipped = new RecommendationInput.Builder().equipment("壶铃", "TRX 悬挂带", "哑铃")
                .intensity(Intensity.MEDIUM).unknownWorkout().build();
        List<Exercise> safe = new RecommendationEngine(seeds).safeCandidates(equipped);
        WorkoutPlan p = AdHocPlanner.plan(safe, new AdHocPlanner.Request().minutes(25).intensity(Intensity.MEDIUM));
        check(AdHocPlanner.plan(safe, new AdHocPlanner.Request().intent(AdHocIntent.parse("恢复"))).intensity() == Intensity.LOW, "Recovery must be labelled low even when the previous mode was daily");
        Set<String> roles = new HashSet<>(), tools = new HashSet<>();
        for (WorkoutItem item : p.items()) {
            roles.add(TrainingSelection.role(item.exercise())); tools.addAll(item.exercise().equipment());
            System.out.println(item.exercise().name() + " " + item.prescription().compactLabel());
        }
        check(roles.containsAll(Arrays.asList("髋铰链", "推", "拉", "蹲", "核心")), "25-minute daily must cover main patterns before accessories");
        check(tools.containsAll(Arrays.asList("壶铃", "TRX 悬挂带", "哑铃")), "Equipment selection must reach actual workout");
        check(p.items().stream().noneMatch(i -> i.exercise().id().equals("exercise_wall_pushup")), "Daily must not default to wall pushups when loaded options available");
        check(p.estimatedMinutes() >= 20 && p.estimatedMinutes() <= 25, "Meaningful dose within 25-minute budget");
        WorkoutPlan again = AdHocPlanner.plan(safe, new AdHocPlanner.Request().minutes(25).intensity(Intensity.MEDIUM));
        for (int i = 0; i < p.items().size(); i++) check(p.items().get(i).exercise().id().equals(again.items().get(i).exercise().id()), "Stable selection");
        for (int minutes : new int[]{3,8,15,25,40}) for (double pace : new double[]{.6,1,1.8}) {
            WorkoutPlan budget = AdHocPlanner.plan(safe, new AdHocPlanner.Request().minutes(minutes).paceFactor(pace));
            check(new SessionTimeModel(pace).sessionSeconds(budget.items()) <= minutes * 60, "Never exceed time budget");
        }
        List<Exercise> body = new RecommendationEngine(seeds).safeCandidates(new RecommendationInput.Builder().build());
        check(body.stream().noneMatch(TrainingSelection::loaded), "Empty equipment cannot unlock every machine");
        check(find(seeds,"exercise_pushup").hasAvailableEquipment(Arrays.asList("哑铃")), "Bodyweight remains available even when unchecked");
        RecommendationInput painful = new RecommendationInput.Builder().equipment("壶铃", "TRX 悬挂带", "哑铃")
                .pain(PainPoint.lowerBack(PainSeverity.SEVERE)).build();
        // Verify via the same hard filter used before the planner.
        check(new RecommendationEngine(seeds).safeCandidates(painful).stream().noneMatch(e -> e.jointStress("lower_back").isAtLeast(StressLevel.MEDIUM)), "Severe pain must remain a hard filter");
        WorkoutItem a = new WorkoutItem(find(seeds,"exercise_kettlebell_deadlift"), new Prescription(1,"12","7-8",20),false,"16 kg",20,"16 kg");
        WorkoutItem b = new WorkoutItem(find(seeds,"exercise_trx_row"),Prescription.hold(1,45,"7",10,false),false,"脚前移",10);
        WorkoutRoutine routine = new WorkoutRoutine("r","我的循环","来源",true,3,60,Arrays.asList(a,b));
        List<WorkoutItem> expanded = routine.expand();
        check(expanded.size()==6, "Circuit must execute A B A B A B, not AAA BBB");
        for(int i=0;i<6;i++) check(expanded.get(i).exercise().id().equals(i%2==0?a.exercise().id():b.exercise().id()), "Circuit order");
        check(expanded.get(0).restAfterSeconds()==20 && expanded.get(1).restAfterSeconds()==60 && expanded.get(5).restAfterSeconds()==0,"Exercise/round rests and no trailing rest");
        check(expanded.get(0).weight().equals("16 kg") && expanded.get(0).reason().contains("16 kg") && expanded.get(2).reason().contains("第 2"),"Weight and round retained");
        int work = 3*(new SessionTimeModel().itemSeconds(a.prescription())+new SessionTimeModel().itemSeconds(b.prescription()));
        check(new SessionTimeModel().sessionSeconds(expanded)==work+3*20+2*60,"Estimate includes inter-exercise/round rests");
        check(new WorkoutRoutine("s","顺序","",false,1,0,Arrays.asList(a,b)).expand().size()==2,"Straight sets do not repeat rounds");
        try { new WorkoutRoutine("x","","",true,3,60,Arrays.asList(a)); throw new AssertionError("Blank title accepted"); } catch(IllegalArgumentException expected) {}
        check(new SessionTimeModel().sessionSeconds(Arrays.asList(a)) == new SessionTimeModel().itemSeconds(a.prescription()), "Last exercise has no trailing rest in estimate");
        Exercise tap = new Exercise.Builder("tap", "交替拍肩").regions("核心").build();
        Prescription tapDose = ExerciseTempo.effective(tap, new Prescription(3, "8-12", "7-8", 30));
        check(tapDose.perSide() && tapDose.repsLow() == 10 && tapDose.repsHigh() == 15, "Shoulder taps specify 10-15 each side, 20-30 total");
        Exercise plank = new Exercise.Builder("plank", "平板支撑").build();
        check(ExerciseTempo.effective(plank, Prescription.hold(2, 20, "", 10, false)).holdSeconds() == 20, "An explicit hold duration is never re-inferred as 30 seconds");
        check(p.items().stream().allMatch(i -> i.prescription().restSeconds() <= 30 && i.restAfterSeconds() == 75), "Daily rest defaults reach every generated item");
        System.out.println("TrainingRoutineTest: all checks passed");
    }
}
