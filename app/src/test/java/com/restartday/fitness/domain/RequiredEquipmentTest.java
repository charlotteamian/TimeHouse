package com.restartday.fitness.domain;

import java.util.Arrays;
import java.util.Collections;

public final class RequiredEquipmentTest {
    public static void main(String[] args) {
        Exercise row = new Exercise.Builder("row", "扶凳划船").equipment("哑铃")
                .requiredEquipment("平板训练凳").evidence(EvidenceStatus.DEFAULT_LIBRARY).build();
        Exercise dip = new Exercise.Builder("dip", "屈膝凳上臂屈伸").equipment("自重")
                .requiredEquipment("平板训练凳").evidence(EvidenceStatus.DEFAULT_LIBRARY).build();
        require(!row.hasAvailableEquipment(Arrays.asList("哑铃")), "Dumbbells alone must not satisfy bench row");
        require(!row.hasAvailableEquipment(Arrays.asList("平板训练凳")), "Bench alone must not satisfy dumbbell row");
        require(row.hasAvailableEquipment(Arrays.asList("哑铃", "平板训练凳")), "Both row requirements should pass");
        require(!dip.hasAvailableEquipment(Arrays.asList("自重")), "Bodyweight must not bypass bench requirement");
        require(dip.hasAvailableEquipment(Arrays.asList("平板训练凳")), "Bench is sufficient for bodyweight dip");
        require(!row.hasAvailableEquipment(Arrays.asList("哑铃", "下斜训练凳")), "Bench configurations are not interchangeable");
        Exercise both = new Exercise.Builder("both", "双支撑").equipment("自重").requiredEquipment("A", "B").build();
        require(!both.hasAvailableEquipment(Arrays.asList("A")) && both.hasAvailableEquipment(Arrays.asList("A", "B")), "All additional supports must be available");
        Exercise free = new Exercise.Builder("free", "徒手").equipment("自重").build();
        require(free.hasAvailableEquipment(Collections.emptyList()), "Plain bodyweight remains available");
        Exercise choice = new Exercise.Builder("choice", "旧器械选择").equipment("哑铃", "弹力带").build();
        require(choice.hasAvailableEquipment(Arrays.asList("弹力带")), "Existing alternative equipment keeps OR semantics");
        RecommendationEngine engine = new RecommendationEngine(Arrays.asList(row, dip));
        require(engine.safeCandidates(new RecommendationInput.Builder().equipment("哑铃").build()).isEmpty(), "Recommendation safety filter enforces supports");
        require(engine.safeCandidates(new RecommendationInput.Builder().equipment("哑铃", "平板训练凳").build()).size()==2, "Both exercises become eligible with required equipment");
        System.out.println("RequiredEquipmentTest: all tests passed");
    }
    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
