package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.List;

public final class SeedExercises {
    private SeedExercises() {
    }

    public static List<Exercise> defaultExercises() {
        List<Exercise> exercises = new ArrayList<Exercise>();

        exercises.add(base("exercise_lat_pulldown", "高位下拉")
                .media(motion("lat_pulldown"))
                .regions("背")
                .patterns("拉", "垂直拉")
                .equipment("高位下拉器", "固定器械")
                .difficulty("beginner_to_intermediate")
                .stress("shoulder", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.LOW)
                .stress("knee", StressLevel.LOW)
                .instructions("坐稳并握住把手，保持躯干稳定。", "把手向上胸方向下拉，感受背部发力。", "控制还原，避免耸肩和大幅后仰。")
                .mistakes("过度后仰", "耸肩", "用手臂主导发力")
                .substitutions("坐姿划船", "弹力带下拉", "辅助引体向上")
                .build());

        exercises.add(base("exercise_band_row", "弹力带划船")
                .media(motion("band_row"))
                .regions("背")
                .patterns("拉", "水平拉")
                .equipment("弹力带")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("固定弹力带，身体保持直立。", "肘部向后拉，肩胛骨轻轻后收。", "慢速还原，保持颈肩放松。")
                .substitutions("坐姿划船", "单臂哑铃划船")
                .prescriptions(new Prescription(2, "10-15", "5-6", 60),
                        new Prescription(3, "10-15", "6-7", 75),
                        new Prescription(4, "8-12", "7-8", 90))
                .build());

        exercises.add(base("exercise_one_arm_dumbbell_row", "单臂哑铃划船")
                .media(motion("one_arm_dumbbell_row"))
                .regions("背")
                .patterns("拉", "水平拉")
                .equipment("哑铃")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.MEDIUM)
                .instructions("一手支撑，躯干稳定。", "哑铃沿身体侧面向上拉。", "避免旋转身体或塌腰。")
                .substitutions("弹力带划船", "坐姿划船")
                .build());

        exercises.add(base("exercise_seated_row", "坐姿划船")
                .media(motion("seated_row"))
                .regions("背")
                .patterns("拉", "水平拉")
                .equipment("固定器械")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("坐稳，脚踩踏板。", "向腹部方向拉手柄，肩胛骨后收。", "保持背部中立，不耸肩。")
                .substitutions("弹力带划船", "单臂哑铃划船")
                .build());

        exercises.add(base("exercise_band_pulldown", "弹力带下拉")
                .media(motion("band_pulldown"))
                .regions("背")
                .patterns("拉", "垂直拉")
                .equipment("弹力带")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("将弹力带固定在高处。", "肘部向身体两侧下拉。", "控制回弹，避免耸肩。")
                .substitutions("高位下拉", "辅助引体向上")
                .build());

        exercises.add(base("exercise_bent_over_barbell_row", "杠铃俯身划船")
                .media(motion("bent_over_barbell_row"))
                .regions("背")
                .patterns("拉", "水平拉")
                .equipment("杠铃")
                .difficulty("intermediate")
                .stress("shoulder", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.HIGH)
                .instructions("髋部折叠，背部保持中立。", "杠铃向下胸或上腹方向拉。", "保持核心张力。")
                .substitutions("坐姿划船", "胸托划船", "弹力带划船")
                .build());

        exercises.add(base("exercise_face_pull", "面拉")
                .media(motion("face_pull"))
                .regions("肩", "背")
                .patterns("拉", "肩胛稳定")
                .equipment("弹力带", "固定器械")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("弹力带固定在面部高度。", "向面部拉，肘部打开。", "感受后束和肩胛稳定。")
                .substitutions("俯身 Y/T/W", "弹力带外旋")
                .build());

        exercises.add(base("exercise_wall_pushup", "墙壁俯卧撑")
                .media(motion("wall_pushup"))
                .regions("胸", "手臂")
                .patterns("推", "水平推")
                .equipment("自重")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("双手扶墙，身体成一直线。", "屈肘靠近墙面，再推回。", "保持动作可控。")
                .substitutions("上斜俯卧撑", "器械推胸")
                .prescriptions(new Prescription(1, "8-12", "5", 60),
                        new Prescription(2, "10-15", "5-6", 75),
                        new Prescription(3, "10-15", "6-7", 90))
                .build());

        exercises.add(base("exercise_incline_pushup", "上斜俯卧撑")
                .media(motion("incline_pushup"))
                .regions("胸", "手臂")
                .patterns("推", "水平推")
                .equipment("自重")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("双手撑在稳定高台。", "身体保持一条直线。", "下放和推起都保持控制。")
                .substitutions("墙壁俯卧撑", "标准俯卧撑")
                .build());

        exercises.add(base("exercise_dumbbell_bench_press", "哑铃卧推")
                .media(motion("dumbbell_bench_press"))
                .regions("胸")
                .patterns("推", "水平推")
                .equipment("哑铃")
                .stress("shoulder", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.LOW)
                .instructions("仰卧，肩胛稳定。", "哑铃下放到胸侧。", "向上推起，避免耸肩。")
                .substitutions("上斜俯卧撑", "坐姿推胸")
                .build());

        exercises.add(base("exercise_seated_chest_press", "坐姿推胸")
                .media(motion("seated_chest_press"))
                .regions("胸")
                .patterns("推", "水平推")
                .equipment("固定器械")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("调好座椅高度。", "向前推手柄。", "控制还原，不耸肩。")
                .substitutions("墙壁俯卧撑", "哑铃卧推")
                .build());

        exercises.add(base("exercise_seated_shoulder_press", "坐姿肩推")
                .media(motion("seated_shoulder_press"))
                .regions("肩")
                .patterns("推", "垂直推")
                .equipment("哑铃", "固定器械")
                .difficulty("intermediate")
                .stress("shoulder", StressLevel.HIGH)
                .stress("lower_back", StressLevel.MEDIUM)
                .instructions("坐稳并收紧核心。", "从肩部位置向上推。", "避免疼痛范围和过度耸肩。")
                .substitutions("墙壁俯卧撑", "坐姿推胸", "弹力带外旋")
                .build());

        exercises.add(base("exercise_band_external_rotation", "弹力带外旋")
                .media(motion("band_external_rotation"))
                .regions("肩")
                .patterns("肩袖", "稳定")
                .equipment("弹力带")
                .stress("shoulder", StressLevel.LOW)
                .stress("lower_back", StressLevel.NONE)
                .instructions("肘部贴近身体侧面。", "向外旋转小臂。", "轻阻力慢速完成。")
                .substitutions("面拉")
                .prescriptions(new Prescription(1, "12-15", "4-5", 45),
                        new Prescription(2, "12-15", "5-6", 60),
                        new Prescription(3, "12-15", "6", 75))
                .build());

        exercises.add(base("exercise_sit_to_stand", "坐站")
                .media(motion("sit_to_stand"))
                .regions("腿", "臀")
                .patterns("蹲", "双腿蹲")
                .equipment("自重")
                .stress("knee", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("坐在稳定椅子前缘。", "脚掌踩稳，站起后再坐回。", "膝盖跟随脚尖方向。")
                .substitutions("箱式深蹲", "杯式深蹲")
                .prescriptions(new Prescription(1, "8-10", "5", 60),
                        new Prescription(2, "8-12", "6", 75),
                        new Prescription(3, "8-12", "7", 90))
                .build());

        exercises.add(base("exercise_goblet_squat", "杯式深蹲")
                .media(motion("goblet_squat"))
                .regions("腿", "臀")
                .patterns("蹲", "双腿蹲")
                .equipment("哑铃", "壶铃")
                .stress("knee", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.LOW)
                .instructions("双手抱住哑铃或壶铃。", "下蹲到可控深度。", "站起时保持脚掌稳定。")
                .substitutions("坐站", "腿举")
                .build());

        exercises.add(base("exercise_glute_bridge", "臀桥")
                .media(motion("glute_bridge"))
                .regions("臀", "腿")
                .patterns("髋铰链", "髋伸展")
                .equipment("自重", "杠铃")
                .stress("knee", StressLevel.LOW)
                .stress("lower_back", StressLevel.LOW)
                .instructions("仰卧屈膝，脚踩地。", "收紧臀部抬髋。", "避免腰部过度反弓。")
                .substitutions("鸟狗", "罗马尼亚硬拉")
                .build());

        exercises.add(base("exercise_romanian_deadlift", "罗马尼亚硬拉")
                .media(motion("romanian_deadlift"))
                .regions("臀", "腿")
                .patterns("髋铰链")
                .equipment("哑铃", "杠铃")
                .difficulty("intermediate")
                .stress("lower_back", StressLevel.HIGH)
                .stress("knee", StressLevel.LOW)
                .instructions("髋部向后折叠。", "背部保持中立。", "感受臀腿后侧拉伸后站起。")
                .substitutions("臀桥", "鸟狗")
                .build());

        exercises.add(base("exercise_step_up", "台阶上步")
                .media(motion("step_up"))
                .regions("腿", "臀")
                .patterns("单腿")
                .equipment("自重", "哑铃")
                .stress("knee", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.LOW)
                .instructions("选择稳定台阶。", "一脚踩稳后上步。", "缓慢下放，保持膝盖方向。")
                .substitutions("坐站", "杯式深蹲")
                .build());

        exercises.add(base("exercise_dead_bug", "死虫")
                .media(motion("dead_bug"))
                .regions("核心")
                .patterns("抗伸展", "稳定")
                .equipment("自重")
                .stress("lower_back", StressLevel.LOW)
                .stress("shoulder", StressLevel.NONE)
                .instructions("仰卧，腰背轻贴地。", "对侧手脚慢慢伸展。", "保持呼吸和骨盆稳定。")
                .substitutions("鸟狗", "平板支撑")
                .prescriptions(new Prescription(1, "6-8/侧", "4-5", 45),
                        new Prescription(2, "8-10/侧", "5-6", 60),
                        new Prescription(3, "8-12/侧", "6-7", 75))
                .build());

        exercises.add(base("exercise_plank", "平板支撑")
                .media(motion("plank"))
                .regions("核心")
                .patterns("抗伸展", "稳定")
                .equipment("自重")
                .stress("lower_back", StressLevel.MEDIUM)
                .stress("shoulder", StressLevel.LOW)
                .instructions("前臂撑地，身体成一直线。", "保持自然呼吸。", "腰部不塌陷。")
                .substitutions("死虫", "鸟狗")
                .build());

        exercises.add(base("exercise_pallof_press", "帕洛夫抗旋推")
                .media(motion("pallof_press"))
                .regions("核心")
                .patterns("抗旋转", "稳定")
                .equipment("弹力带", "固定器械")
                .stress("lower_back", StressLevel.LOW)
                .stress("shoulder", StressLevel.LOW)
                .instructions("侧身站立，弹力带在胸前。", "双手向前推出并抵抗旋转。", "控制收回。")
                .substitutions("侧桥", "死虫")
                .build());

        exercises.add(base("exercise_bird_dog", "鸟狗")
                .media(motion("bird_dog"))
                .regions("核心", "臀")
                .patterns("稳定", "髋伸展")
                .equipment("自重")
                .stress("lower_back", StressLevel.LOW)
                .stress("shoulder", StressLevel.LOW)
                .instructions("四点支撑。", "对侧手脚缓慢伸展。", "保持骨盆稳定。")
                .substitutions("死虫", "臀桥")
                .build());

        exercises.add(base("exercise_dumbbell_curl", "哑铃弯举")
                .media(motion("dumbbell_curl"))
                .regions("手臂")
                .patterns("肘屈")
                .equipment("哑铃")
                .stress("elbow", StressLevel.MEDIUM)
                .stress("shoulder", StressLevel.LOW)
                .instructions("手持哑铃，肘部靠近身体。", "弯举至可控高度。", "慢速下放。")
                .substitutions("弹力带弯举")
                .build());

        exercises.add(base("custom_inverted_row_unverified", "自定义倒立划船")
                .evidence(EvidenceStatus.USER_UNVERIFIED)
                .media(motion("inverted_row"))
                .regions("背")
                .patterns("拉", "水平拉")
                .equipment("神秘器械")
                .stress("shoulder", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.LOW)
                .instructions("用户导入动作，尚未审核。")
                .substitutions("弹力带划船")
                .build());

        exercises.add(base("exercise_kettlebell_deadlift", "壶铃硬拉")
                .regions("臀", "腿").patterns("髋铰链").equipment("壶铃")
                .stress("lower_back", StressLevel.MEDIUM).stress("knee", StressLevel.LOW)
                .instructions("壶铃放在两脚之间，髋向后折叠，保持背部中立。", "脚掌压地，髋膝伸展站起，手臂只负责握持。", "髋向后移，控制壶铃落回地面；先以可控重量练习。")
                .build());
        exercises.add(base("exercise_trx_row", "TRX 反向划船")
                .regions("背", "手臂").patterns("拉", "水平拉").equipment("TRX 悬挂带")
                .stress("shoulder", StressLevel.MEDIUM).stress("lower_back", StressLevel.LOW)
                .instructions("确认锚点牢固，握住把手后倾，身体保持一条直线。", "肘向后拉，将胸部带向把手，避免耸肩。", "控制还原；身体越直立越轻松，用脚的位置调节难度。")
                .build());
        exercises.add(base("exercise_dumbbell_overhead_press", "哑铃推举")
                .regions("肩", "手臂").patterns("推", "垂直推").equipment("哑铃")
                .stress("shoulder", StressLevel.MEDIUM).stress("lower_back", StressLevel.MEDIUM)
                .instructions("双脚站稳，哑铃位于肩侧，收紧腹部。", "向上推起，肋骨不要外翻，不用腰后仰代偿。", "控制下降到肩侧；选择末几次费力但仍能保持姿势的重量。")
                .build());
        exercises.add(base("exercise_kettlebell_swing", "壶铃摇摆")
                .regions("臀", "腿").patterns("髋铰链", "爆发力").equipment("壶铃").difficulty("intermediate")
                .stress("lower_back", StressLevel.HIGH).stress("shoulder", StressLevel.MEDIUM)
                .instructions("先掌握髋铰链和壶铃硬拉；用能稳定控制的重量。", "髋向后折叠，壶铃从腿间后摆，伸髋带动壶铃到胸前附近。", "手臂不主动上提，不后仰顶腰；动作变形就停组。")
                .build());
        exercises.add(base("exercise_jumping_jack", "开合跳")
                .regions("有氧").patterns("有氧").equipment("自重")
                .stress("knee", StressLevel.MEDIUM)
                .instructions("轻跳打开双脚，同时双臂举起。", "轻柔落地后回到起始位；不适时改为交替向侧迈步。")
                .prescriptions(Prescription.hold(1, 30, "4-5", 30, false),
                        Prescription.hold(1, 60, "6-7", 30, false), Prescription.hold(1, 60, "7-8", 30, false))
                .build());
        exercises.add(base("exercise_bodyweight_squat", "徒手深蹲")
                .regions("腿", "臀").patterns("蹲").equipment("自重")
                .stress("knee", StressLevel.MEDIUM)
                .instructions("双脚站稳，髋膝同时屈曲。", "膝盖朝脚尖方向，蹲至能够稳定控制的位置，再站起。")
                .build());
        exercises.add(base("exercise_pushup", "俯卧撑")
                .media("raw:dataset_motion_0662")
                .regions("胸", "手臂").patterns("推", "水平推").equipment("自重")
                .stress("shoulder", StressLevel.MEDIUM).stress("lower_back", StressLevel.LOW)
                .instructions("双手撑地，身体保持一条直线。", "屈肘控制下降后推起，不塌腰；无法完成时抬高手部支撑面。")
                .build());
        return exercises;
    }

    private static Exercise.Builder base(String id, String name) {
        return new Exercise.Builder(id, name)
                .evidence(EvidenceStatus.GUIDELINE_BACKED)
                .evidenceRefs("ACSM resistance training guidance", "HHS Physical Activity Guidelines", "ACE Exercise Library")
                .prescriptions(new Prescription(2, "10-12", "5-6", 75),
                        new Prescription(3, "8-12", "6-8", 90),
                        new Prescription(4, "6-10", "7-8", 120));
    }

    private static String motion(String key) {
        return "raw:motion_" + key;
    }
}
