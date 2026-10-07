package com.restartday.fitness.app;

import com.restartday.fitness.domain.EvidenceStatus;
import com.restartday.fitness.domain.Exercise;
import com.restartday.fitness.domain.StressLevel;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/** Loads the Chinese, app-normalized snapshot of hasaneyldrm/exercises-dataset. */
public final class ExerciseDatasetLoader {
    public static final String ASSET_NAME = "exercises_1324.json";
    public static final String ID_PREFIX = "dataset_1324_";
    public static final int EXPECTED_COUNT = 1324;
    public static final String SOURCE_LABEL = "默认动作库";

    private ExerciseDatasetLoader() {
    }

    public static List<Exercise> load(InputStream input) throws Exception {
        JSONObject root = new JSONObject(readUtf8(input));
        JSONArray rows = root.getJSONArray("exercises");
        if (rows.length() != EXPECTED_COUNT) {
            throw new IllegalStateException("Expected " + EXPECTED_COUNT + " exercises, got " + rows.length());
        }

        List<Exercise> exercises = new ArrayList<Exercise>(rows.length());
        Set<String> ids = new LinkedHashSet<String>();
        for (int i = 0; i < rows.length(); i++) {
            JSONObject row = rows.getJSONObject(i);
            Exercise exercise = map(row);
            if (!ids.add(exercise.id())) {
                throw new IllegalStateException("Duplicate exercise id: " + exercise.id());
            }
            exercises.add(exercise);
        }
        return exercises;
    }

    private static Exercise map(JSONObject row) {
        String upstreamId = required(row, "id");
        required(row, "name");
        String name = required(row, "name_zh");
        String category = required(row, "category");
        String target = row.optString("target");
        String muscleGroup = row.optString("muscle_group");

        List<String> regions = regions(category, target);
        List<String> primary = uniqueLocalized(target, muscleGroup);
        List<String> secondary = localizedArray(row.optJSONArray("secondary_muscles"));
        List<String> instructions = stringArray(row.optJSONArray("instructions_zh"));
        if (instructions.isEmpty()) {
            instructions.add("上游数据未提供中文步骤，请在验证后补充。");
        }

        Exercise.Builder builder = new Exercise.Builder(ID_PREFIX + upstreamId, name)
                .evidence(EvidenceStatus.DEFAULT_LIBRARY)
                .regions(regions.toArray(new String[0]))
                .patterns((row.has("movement_patterns_zh") ? stringArray(row.optJSONArray("movement_patterns_zh"))
                        : patterns(category, target)).toArray(new String[0]))
                .equipment(localizeEquipment(row.optString("equipment")))
                .requiredEquipment(stringArray(row.optJSONArray("required_equipment_zh")).toArray(new String[0]))
                .primaryMuscles(primary.toArray(new String[0]))
                .secondaryMuscles(secondary.toArray(new String[0]))
                .difficulty("unknown")
                .instructions(instructions.toArray(new String[0]))
                .media(row.optString("media"))
                .source(SOURCE_LABEL + " · MIT · 编号 " + upstreamId)
                .evidenceRefs("Imported dataset metadata; verify technique and risks before recommendation");
        addConservativeStress(builder, category);
        List<String> reviewedPatterns = stringArray(row.optJSONArray("movement_patterns_zh"));
        if (reviewedPatterns.contains("髋铰链") || reviewedPatterns.contains("俯身稳定")) {
            builder.stress("lower_back", StressLevel.MEDIUM);
        }
        if (reviewedPatterns.contains("过顶伸展") || reviewedPatterns.contains("高位支撑")) {
            builder.stress("shoulder", StressLevel.MEDIUM).stress("lower_back", StressLevel.MEDIUM);
        }
        return builder.build();
    }

    private static void addConservativeStress(Exercise.Builder builder, String category) {
        String normalized = category.toLowerCase(Locale.ROOT);
        if ("back".equals(normalized) || "chest".equals(normalized)
                || "shoulders".equals(normalized) || "upper arms".equals(normalized)) {
            builder.stress("shoulder", StressLevel.MEDIUM);
        }
        if ("waist".equals(normalized) || "back".equals(normalized)) {
            builder.stress("lower_back", StressLevel.MEDIUM);
        }
        if ("upper legs".equals(normalized) || "lower legs".equals(normalized)
                || "cardio".equals(normalized)) {
            builder.stress("knee", StressLevel.MEDIUM);
        }
    }

    private static List<String> regions(String category, String target) {
        LinkedHashSet<String> result = new LinkedHashSet<String>();
        String normalized = category.toLowerCase(Locale.ROOT);
        if ("back".equals(normalized)) {
            result.add("背");
        } else if ("cardio".equals(normalized)) {
            result.add("有氧");
        } else if ("chest".equals(normalized)) {
            result.add("胸");
        } else if ("lower arms".equals(normalized) || "upper arms".equals(normalized)) {
            result.add("手臂");
        } else if ("lower legs".equals(normalized) || "upper legs".equals(normalized)) {
            result.add("腿");
        } else if ("neck".equals(normalized)) {
            result.add("颈");
        } else if ("shoulders".equals(normalized)) {
            result.add("肩");
        } else if ("waist".equals(normalized)) {
            result.add("核心");
        } else {
            result.add("其他");
        }
        if ("glutes".equals(target.toLowerCase(Locale.ROOT))) {
            result.add("臀");
        }
        return new ArrayList<String>(result);
    }

    private static List<String> patterns(String category, String target) {
        List<String> result = new ArrayList<String>();
        String normalized = category.toLowerCase(Locale.ROOT);
        String normalizedTarget = target.toLowerCase(Locale.ROOT);
        if ("back".equals(normalized) || "biceps".equals(normalizedTarget)) {
            result.add("拉");
        } else if ("chest".equals(normalized) || "triceps".equals(normalizedTarget)) {
            result.add("推");
        } else if ("upper legs".equals(normalized) || "lower legs".equals(normalized)) {
            result.add("下肢");
        } else if ("waist".equals(normalized)) {
            result.add("核心");
        } else if ("cardio".equals(normalized)) {
            result.add("有氧");
        } else if ("neck".equals(normalized)) {
            result.add("颈部");
        } else {
            result.add("辅助");
        }
        return result;
    }

    private static List<String> uniqueLocalized(String first, String second) {
        LinkedHashSet<String> values = new LinkedHashSet<String>();
        if (first != null && first.trim().length() > 0) {
            values.add(localizeMuscle(first));
        }
        if (second != null && second.trim().length() > 0) {
            values.add(localizeMuscle(second));
        }
        return new ArrayList<String>(values);
    }

    private static List<String> localizedArray(JSONArray array) {
        LinkedHashSet<String> result = new LinkedHashSet<String>();
        if (array != null) {
            for (int i = 0; i < array.length(); i++) {
                String value = array.optString(i).trim();
                if (value.length() > 0) {
                    result.add(localizeMuscle(value));
                }
            }
        }
        return new ArrayList<String>(result);
    }

    private static List<String> stringArray(JSONArray array) {
        List<String> result = new ArrayList<String>();
        if (array != null) {
            for (int i = 0; i < array.length(); i++) {
                String value = array.optString(i).trim();
                if (value.length() > 0) {
                    result.add(value);
                }
            }
        }
        return result;
    }

    private static String localizeEquipment(String value) {
        String key = value == null ? "" : value.toLowerCase(Locale.ROOT);
        if ("body weight".equals(key)) return "自重";
        if ("suspension trainer".equals(key)) return "TRX 悬挂带";
        if ("gymnastic rings".equals(key)) return "吊环";
        if ("pull-up bar".equals(key)) return "单杠";
        if ("dumbbell".equals(key)) return "哑铃";
        if ("barbell".equals(key) || "olympic barbell".equals(key)) return "杠铃";
        if ("ez barbell".equals(key)) return "EZ 杠";
        if ("cable".equals(key) || "leverage machine".equals(key)) return "固定器械";
        if ("band".equals(key) || "resistance band".equals(key)) return "弹力带";
        if ("smith machine".equals(key)) return "史密斯机";
        if ("kettlebell".equals(key)) return "壶铃";
        if ("stability ball".equals(key)) return "瑜伽球";
        if ("medicine ball".equals(key)) return "药球";
        if ("bosu ball".equals(key)) return "BOSU 球";
        if ("rope".equals(key)) return "绳索";
        if ("roller".equals(key) || "wheel roller".equals(key)) return "健腹轮 / 滚轮";
        if ("stationary bike".equals(key)) return "动感单车";
        if ("elliptical machine".equals(key)) return "椭圆机";
        if ("stepmill machine".equals(key)) return "登阶机";
        if ("skierg machine".equals(key)) return "滑雪训练机";
        if ("upper body ergometer".equals(key)) return "上肢功率车";
        if ("sled machine".equals(key)) return "雪橇机";
        if ("hammer".equals(key)) return "大锤";
        if ("tire".equals(key)) return "轮胎";
        if ("trap bar".equals(key)) return "六角杠";
        if ("assisted".equals(key)) return "辅助器械";
        if ("weighted".equals(key)) return "负重";
        return value == null || value.trim().length() == 0 ? "未标注" : value;
    }

    private static String localizeMuscle(String value) {
        String key = value == null ? "" : value.toLowerCase(Locale.ROOT);
        if ("abs".equals(key) || "abdominals".equals(key)) return "腹肌";
        if ("pectorals".equals(key) || "chest".equals(key)) return "胸肌";
        if ("biceps".equals(key)) return "肱二头肌";
        if ("triceps".equals(key)) return "肱三头肌";
        if ("glutes".equals(key)) return "臀肌";
        if ("delts".equals(key) || "deltoids".equals(key)) return "三角肌";
        if ("upper back".equals(key)) return "上背";
        if ("lats".equals(key) || "latissimus dorsi".equals(key)) return "背阔肌";
        if ("calves".equals(key)) return "小腿肌";
        if ("quads".equals(key) || "quadriceps".equals(key)) return "股四头肌";
        if ("forearms".equals(key)) return "前臂";
        if ("hamstrings".equals(key)) return "腘绳肌";
        if ("cardiovascular system".equals(key)) return "心肺系统";
        if ("spine".equals(key)) return "脊柱";
        if ("traps".equals(key) || "trapezius".equals(key)) return "斜方肌";
        if ("adductors".equals(key) || "inner thighs".equals(key) || "groin".equals(key)) return "大腿内收肌群";
        if ("abductors".equals(key)) return "髋外展肌群";
        if ("serratus anterior".equals(key)) return "前锯肌";
        if ("levator scapulae".equals(key)) return "肩胛提肌";
        if ("shoulders".equals(key)) return "肩部";
        if ("obliques".equals(key)) return "腹斜肌";
        if ("hip flexors".equals(key)) return "髋屈肌群";
        if ("core".equals(key)) return "核心肌群";
        if ("lower back".equals(key)) return "下背";
        if ("lower abs".equals(key)) return "下腹肌";
        if ("upper chest".equals(key)) return "上胸肌";
        if ("rotator cuff".equals(key)) return "肩袖肌群";
        if ("rhomboids".equals(key)) return "菱形肌";
        if ("rear deltoids".equals(key)) return "三角肌后束";
        if ("brachialis".equals(key)) return "肱肌";
        if ("ankles".equals(key) || "ankle stabilizers".equals(key)) return "踝关节稳定肌";
        if ("soleus".equals(key)) return "比目鱼肌";
        if ("wrist flexors".equals(key)) return "腕屈肌";
        if ("wrist extensors".equals(key)) return "腕伸肌";
        if ("wrists".equals(key)) return "腕部肌群";
        if ("sternocleidomastoid".equals(key)) return "胸锁乳突肌";
        if ("feet".equals(key)) return "足部肌群";
        if ("shins".equals(key)) return "胫骨前肌群";
        if ("hands".equals(key) || "grip muscles".equals(key)) return "握力肌群";
        return value == null ? "" : value;
    }

    private static String required(JSONObject object, String key) {
        String value = object.optString(key).trim();
        if (value.length() == 0) {
            throw new IllegalArgumentException("Missing " + key);
        }
        return value;
    }

    private static String readUtf8(InputStream input) throws Exception {
        try (InputStream in = input; ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192];
            int read;
            while ((read = in.read(buffer)) != -1) {
                out.write(buffer, 0, read);
            }
            return out.toString(StandardCharsets.UTF_8.name());
        }
    }
}
