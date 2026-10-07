import com.restartday.fitness.domain.Exercise;
import com.restartday.fitness.domain.SeedExercises;
public class ExportSeedCatalog {
    private static String q(String s) { return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r") + "\""; }
    public static void main(String[] args) {
        StringBuilder out = new StringBuilder("[");
        for (Exercise e : SeedExercises.defaultExercises()) {
            if (out.length() > 1) out.append(',');
            out.append("{\"id\":").append(q(e.id())).append(",\"name\":").append(q(e.name()))
                .append(",\"equipment\":").append(q(String.join("、",e.equipment())))
                .append(",\"region\":").append(q(String.join("、",e.targetRegions())))
                .append(",\"media\":").append(q(e.media())).append('}');
        }
        System.out.println(out.append(']'));
    }
}
