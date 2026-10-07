package com.restartday.fitness.app;

import android.content.Context;
import android.graphics.*;
import android.view.View;
import org.json.*;
import java.util.*;

/** Actual stored samples only; large gaps are left disconnected. */
final class HeartRateChart extends View {
    private final List<float[]> points = new ArrayList<>();
    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private float minimum = 250, maximum = 0, duration = 1;
    HeartRateChart(Context context, String json) {
        super(context);
        try {
            JSONArray array = new JSONArray(json);
            for (int i = 0; i < array.length(); i++) {
                JSONArray p = array.getJSONArray(i); float time = (float) p.optDouble(0, -1), bpm = (float) p.optDouble(1, 0);
                if (time >= 0 && bpm >= 25 && bpm <= 250) points.add(new float[]{time, bpm});
            }
        } catch (Exception ignored) { }
        Collections.sort(points, (a, b) -> Float.compare(a[0], b[0]));
        for (float[] p : points) { minimum = Math.min(minimum, p[1]); maximum = Math.max(maximum, p[1]); duration = Math.max(duration, p[0]); }
        setContentDescription("心率变化图，横轴为运动开始后的分钟，纵轴为每分钟心跳次数。共有 " + points.size() + " 个采样点");
    }
    private float dp(float x) { return x * getResources().getDisplayMetrics().density; }
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (points.isEmpty()) return;
        float left = dp(40), top = dp(22), width = getWidth() - left - dp(16), height = getHeight() - top - dp(28);
        float low = Math.max(0, minimum - 5), high = Math.max(low + 20, maximum + 5);
        paint.setTextSize(dp(11)); paint.setStrokeWidth(dp(1));
        for (int i = 0; i <= 2; i++) {
            float y = top + height * i / 2;
            paint.setColor(Color.rgb(227, 235, 231)); canvas.drawLine(left, y, left + width, y, paint);
            paint.setColor(Color.DKGRAY); canvas.drawText("" + Math.round(high - (high - low) * i / 2), 0, y + dp(4), paint);
        }
        canvas.drawText("bpm", 0, dp(12), paint);
        canvas.drawText("0 分", left, getHeight() - dp(5), paint);
        String end = String.format(Locale.CHINA, "%.1f 分", duration / 60);
        canvas.drawText(end, left + width - paint.measureText(end), getHeight() - dp(5), paint);
        paint.setColor(Color.rgb(191, 67, 69)); paint.setStrokeWidth(dp(2));
        float[] last = null;
        for (float[] p : points) {
            float x = left + width * p[0] / duration, y = top + height * (high - p[1]) / (high - low);
            if (last != null && p[0] - last[0] <= 120) canvas.drawLine(left + width * last[0] / duration,
                    top + height * (high - last[1]) / (high - low), x, y, paint);
            canvas.drawCircle(x, y, dp(1.5f), paint); last = p;
        }
    }
}
