package com.restartday.fitness.app;

import android.content.Context;
import android.media.AudioAttributes;
import android.media.AudioFocusRequest;
import android.media.AudioManager;
import android.media.SoundPool;

import com.restartday.fitness.R;

import java.util.HashMap;
import java.util.Map;

/**
 * 训练引导的语音口令。
 *
 * <p>用预生成的短音频 + {@link SoundPool}，不用系统 TextToSpeech：
 * 报数必须踩在秒上，而 TTS 有初始化和排队延迟，"三"经常落到第四秒；
 * 而且国产 ROM 不保证装了中文引擎。词表是固定的，预生成完全够用，还能离线。
 *
 * <p>音频资产由 {@code scripts/generate_voice_cues.py} 生成。
 */
final class VoiceCues {

    /** 同时最多几路音——报数和"换边"可能挨在一起。 */
    private static final int MAX_STREAMS = 3;

    private static final int[] NUMBER_RES = {
            R.raw.voice_num_1, R.raw.voice_num_2, R.raw.voice_num_3, R.raw.voice_num_4,
            R.raw.voice_num_5, R.raw.voice_num_6, R.raw.voice_num_7, R.raw.voice_num_8,
            R.raw.voice_num_9, R.raw.voice_num_10};

    private final Context context;
    private final Map<Integer, Integer> soundIds = new HashMap<Integer, Integer>();
    private SoundPool pool;
    private AudioFocusRequest focusRequest;
    private boolean enabled = true;
    private boolean loaded;

    /**
     * 这里不能马上取 applicationContext：本类是 Activity 的字段，
     * 字段初始化跑在 base context 挂上之前，取到的会是 null。
     */
    VoiceCues(Context context) {
        this.context = context;
    }

    private Context appContext() {
        Context application = context.getApplicationContext();
        return application == null ? context : application;
    }

    void setEnabled(boolean value) {
        enabled = value;
        if (!value) {
            release();
        }
    }

    boolean isEnabled() {
        return enabled;
    }

    /** 进入训练时调用：预加载音频并短暂压低其他音乐的音量。 */
    void begin() {
        if (!enabled) {
            return;
        }
        ensureLoaded();
        requestFocus();
    }

    /** 离开训练时调用。 */
    void end() {
        abandonFocus();
    }

    void ready() {
        play(R.raw.voice_ready);
    }

    void go() {
        play(R.raw.voice_go);
    }

    void switchSide() {
        play(R.raw.voice_switch);
    }

    void done() {
        play(R.raw.voice_done);
    }

    void rest() {
        play(R.raw.voice_rest);
    }

    void next() {
        play(R.raw.voice_next);
    }

    /** 报数，只支持 1-10；超出范围静默忽略。 */
    void count(int value) {
        if (value >= 1 && value <= NUMBER_RES.length) {
            play(NUMBER_RES[value - 1]);
        }
    }

    void release() {
        abandonFocus();
        if (pool != null) {
            pool.release();
            pool = null;
        }
        soundIds.clear();
        loaded = false;
    }

    private void play(int resId) {
        if (!enabled) {
            return;
        }
        ensureLoaded();
        Integer soundId = soundIds.get(resId);
        if (pool != null && soundId != null) {
            pool.play(soundId, 1f, 1f, 1, 0, 1f);
        }
    }

    private void ensureLoaded() {
        if (loaded && pool != null) {
            return;
        }
        AudioAttributes attributes = new AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_ASSISTANCE_SONIFICATION)
                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                .build();
        pool = new SoundPool.Builder()
                .setMaxStreams(MAX_STREAMS)
                .setAudioAttributes(attributes)
                .build();
        soundIds.clear();
        int[] all = {R.raw.voice_ready, R.raw.voice_go, R.raw.voice_switch,
                R.raw.voice_done, R.raw.voice_rest, R.raw.voice_next};
        for (int resId : all) {
            soundIds.put(resId, pool.load(appContext(), resId, 1));
        }
        for (int resId : NUMBER_RES) {
            soundIds.put(resId, pool.load(appContext(), resId, 1));
        }
        loaded = true;
    }

    /**
     * 压低而不是打断其他音频：很多人一边放歌一边练，
     * TRANSIENT_MAY_DUCK 让口令能听见又不打断音乐。
     */
    private void requestFocus() {
        if (focusRequest != null) {
            return;
        }
        AudioManager manager = (AudioManager) appContext().getSystemService(Context.AUDIO_SERVICE);
        if (manager == null) {
            return;
        }
        focusRequest = new AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
                .setAudioAttributes(new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_ASSISTANCE_SONIFICATION)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                        .build())
                .build();
        manager.requestAudioFocus(focusRequest);
    }

    private void abandonFocus() {
        if (focusRequest == null) {
            return;
        }
        AudioManager manager = (AudioManager) appContext().getSystemService(Context.AUDIO_SERVICE);
        if (manager != null) {
            manager.abandonAudioFocusRequest(focusRequest);
        }
        focusRequest = null;
    }
}
