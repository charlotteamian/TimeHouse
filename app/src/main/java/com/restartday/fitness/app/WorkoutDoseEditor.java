package com.restartday.fitness.app;

import android.app.AlertDialog;
import android.content.Context;
import android.text.InputType;
import android.widget.*;
import com.restartday.fitness.domain.Prescription;

/** One editor shared by previews, active training, routines and recorded results. */
final class WorkoutDoseEditor {
    interface Save { void save(Prescription dose, int restAfter, String weight, int completed); }
    static void show(Context context, String name, Prescription initial, int after, String load,
            int completed, int minimumSets, Save save) {
        LinearLayout box = new LinearLayout(context); box.setOrientation(LinearLayout.VERTICAL);
        int padding = (int) (18 * context.getResources().getDisplayMetrics().density);
        box.setPadding(padding, 0, padding, padding);
        if (initial == null) {
            TextView hint = new TextView(context);
            hint.setText("旧记录没有保存次数和重量，请按实际训练补填。"
                    + (completed > 0 ? "计划组数先按已记录的完成组数填入，可修改。" : "请同时填写计划组数。"));
            box.addView(hint);
        }
        EditText sets = field(box, "计划组数", initial != null ? "" + initial.sets()
                : completed > 0 ? "" + completed : "", true);
        EditText done = completed < 0 ? null : field(box, "实际完成组数", "" + completed, true);
        CheckBox timed = new CheckBox(context); timed.setText("按秒计时"); timed.setChecked(initial != null && initial.kind() == Prescription.Kind.HOLD); box.addView(timed);
        EditText dose = field(box, "每组次数或秒数", initial == null ? "" : initial.kind() == Prescription.Kind.HOLD ? "" + initial.holdSeconds() : initial.reps().replace("/侧", ""), false);
        TextView hint = new TextView(context); hint.setText("计次可填 30 或 10-15；交替动作选择每侧时，左右分别计数。"); box.addView(hint);
        CheckBox side = new CheckBox(context); side.setText("每侧次数 / 秒数（左右各做）"); side.setChecked(initial != null && initial.perSide()); box.addView(side);
        EditText rest = field(box, "组间休息（秒）", initial == null ? "30" : "" + initial.restSeconds(), true);
        EditText restAfter = field(box, "动作间休息（秒）", "" + after, true);
        EditText weight = field(box, "重量（选填，如单只 5 kg）", load, false);
        EditText rpe = field(box, "目标 RPE（选填）", initial == null ? "" : initial.rpe(), false);
        ScrollView scroll = new ScrollView(context); scroll.addView(box);
        AlertDialog dialog = new AlertDialog.Builder(context).setTitle(name + " · 训练安排").setView(scroll)
                .setNegativeButton("取消", null).setPositiveButton("保存安排", null).create();
        dialog.setOnShowListener(d -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            try {
                for (EditText input : new EditText[]{sets, done, dose, rest, restAfter})
                    if (input != null) input.setError(null);
                int n = integer(sets, Math.max(1, minimumSets), 20), restValue = integer(rest, 0, 600), next = integer(restAfter, 0, 600);
                String value = dose.getText().toString().trim();
                if (!value.matches("[0-9]+(-[0-9]+)?")) throw new InputError(dose, "次数填整数或区间，秒数填整数");
                String bounds = timed.isChecked() ? "计时请填 5–3600 秒" : "次数请填 1–500，区间上限不能小于下限";
                String[] range = value.split("-"); int lo, hi;
                try { lo = Integer.parseInt(range[0]); hi = range.length == 2 ? Integer.parseInt(range[1]) : lo; }
                catch (NumberFormatException e) { throw new InputError(dose, bounds); }
                if (timed.isChecked() ? range.length != 1 || lo < 5 || lo > 3600 : lo < 1 || hi < lo || hi > 500)
                    throw new InputError(dose, bounds);
                Prescription p = timed.isChecked() ? Prescription.hold(n, lo, rpe.getText().toString().trim(), restValue, side.isChecked())
                        : new Prescription(n, value, rpe.getText().toString().trim(), restValue).withPerSide(side.isChecked());
                if (initial != null) p = p.withSecondsPerRep(initial.secondsPerRep());
                int finished = done == null ? -1 : integer(done, 0, n);
                save.save(p, next, weight.getText().toString().trim(), finished);
                dialog.dismiss();
            } catch (InputError e) {
                e.field.requestFocus();
                e.field.setError(e.getMessage());
                e.field.post(() -> e.field.requestRectangleOnScreen(
                        new android.graphics.Rect(0, 0, e.field.getWidth(), e.field.getHeight()), true));
            } catch (RuntimeException e) {
                android.util.Log.e("WorkoutDoseEditor", "Unable to save workout dose", e);
                Toast.makeText(context, "保存失败，请重试；已填写的内容仍保留", Toast.LENGTH_LONG).show();
            }
        }));
        dialog.show();
    }
    private static int integer(EditText field, int min, int max) {
        String raw = field.getText().toString().trim(), name = field.getContentDescription().toString();
        if (raw.isEmpty()) throw new InputError(field, "请填写" + name);
        if (!raw.matches("[0-9]+")) throw new InputError(field, name + "请填写整数");
        int value;
        try { value = Integer.parseInt(raw); }
        catch (NumberFormatException e) { throw new InputError(field, name + "须为 " + min + "–" + max); }
        if (value < min || value > max) throw new InputError(field, name + "须为 " + min + "–" + max);
        return value;
    }
    private static final class InputError extends IllegalArgumentException {
        final EditText field;
        InputError(EditText field, String message) { super(message); this.field = field; }
    }
    private static EditText field(LinearLayout box, String name, String value, boolean numeric) {
        TextView label = new TextView(box.getContext()); label.setText(name); box.addView(label);
        EditText input = new EditText(box.getContext()); input.setContentDescription(name); input.setSingleLine(true);
        input.setInputType(numeric ? InputType.TYPE_CLASS_NUMBER : InputType.TYPE_CLASS_TEXT);
        input.setText(value == null ? "" : value); box.addView(input); return input;
    }
}
