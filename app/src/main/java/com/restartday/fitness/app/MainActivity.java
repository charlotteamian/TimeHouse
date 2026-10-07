package com.restartday.fitness.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.res.ColorStateList;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.ImageDecoder;
import android.graphics.Movie;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.Typeface;
import android.graphics.drawable.AnimatedImageDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.RippleDrawable;
import android.graphics.Outline;
import android.media.AudioManager;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.os.Bundle;
import android.os.OutcomeReceiver;
import android.os.SystemClock;
import android.text.InputType;
import android.view.Gravity;
import android.view.inputmethod.EditorInfo;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewOutlineProvider;
import android.view.WindowInsets;
import android.view.WindowManager;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.Chronometer;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.ScrollView;
import android.widget.Space;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.provider.OpenableColumns;
import android.webkit.MimeTypeMap;

import com.restartday.fitness.domain.ActivityLevel;
import com.restartday.fitness.domain.AdHocIntent;
import com.restartday.fitness.domain.AdHocPlanner;
import com.restartday.fitness.domain.AssessmentInput;
import com.restartday.fitness.domain.AssessmentResult;
import com.restartday.fitness.domain.BuiltinRecipe;
import com.restartday.fitness.domain.DailyGap;
import com.restartday.fitness.domain.DayFoodLog;
import com.restartday.fitness.domain.EnergyPlan;
import com.restartday.fitness.domain.EvidenceStatus;
import com.restartday.fitness.domain.Exercise;
import com.restartday.fitness.domain.ExerciseTempo;
import com.restartday.fitness.domain.FitnessAssessment;
import com.restartday.fitness.domain.FoodGroup;
import com.restartday.fitness.domain.FoodLogEntry;
import com.restartday.fitness.domain.GuidelineRefs;
import com.restartday.fitness.domain.HeartRateStats;
import com.restartday.fitness.domain.Intensity;
import com.restartday.fitness.domain.MealDraft;
import com.restartday.fitness.domain.MealPreset;
import com.restartday.fitness.domain.NutritionPlanner;
import com.restartday.fitness.domain.NutritionProfile;
import com.restartday.fitness.domain.PagodaTargets;
import com.restartday.fitness.domain.PainPoint;
import com.restartday.fitness.domain.PainSeverity;
import com.restartday.fitness.domain.PlanGoal;
import com.restartday.fitness.domain.Prescription;
import com.restartday.fitness.domain.ProgramBuilder;
import com.restartday.fitness.domain.ProgramComposer;
import com.restartday.fitness.domain.ProgramFocus;
import com.restartday.fitness.domain.ProgramPhase;
import com.restartday.fitness.domain.ProgramSchedule;
import com.restartday.fitness.domain.RecipeScorer;
import com.restartday.fitness.domain.RecipeSources;
import com.restartday.fitness.domain.RecoveryState;
import com.restartday.fitness.domain.RecommendationEngine;
import com.restartday.fitness.domain.RecommendationInput;
import com.restartday.fitness.domain.ScheduledSession;
import com.restartday.fitness.domain.SeedExercises;
import com.restartday.fitness.domain.SessionTimeModel;
import com.restartday.fitness.domain.StressLevel;
import com.restartday.fitness.domain.TrainingLevel;
import com.restartday.fitness.domain.TrainingLoad;
import com.restartday.fitness.domain.TrainingProgram;
import com.restartday.fitness.domain.WeeklyVolumeLedger;
import com.restartday.fitness.domain.WorkoutItem;
import com.restartday.fitness.domain.WorkoutRoutine;
import com.restartday.fitness.domain.TrainingSelection;
import com.restartday.fitness.domain.WorkoutPlan;
import com.restartday.fitness.domain.WorkoutClock;
import com.restartday.fitness.R;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class MainActivity extends Activity {
    private static final int BG = Color.rgb(246, 247, 242);
    private static final int SURFACE = Color.WHITE;
    private static final int INK = Color.rgb(31, 41, 37);
    private static final int MUTED = Color.rgb(91, 104, 99);
    private static final int GREEN = Color.rgb(47, 125, 98);
    private static final int GREEN_SOFT = Color.rgb(219, 239, 229);
    private static final int CORAL = Color.rgb(195, 87, 67);
    private static final int BLUE = Color.rgb(49, 91, 133);
    private static final int AMBER = Color.rgb(198, 149, 56);
    private static final int LINE = Color.rgb(221, 226, 218);

    /** ISO 星期（1=周一）对应的中文名。 */
    private static final String[] WEEKDAY_LABELS = {
            "周一", "周二", "周三", "周四", "周五", "周六", "周日"};
    private static final String[] WEEKDAY_SHORT = {"一", "二", "三", "四", "五", "六", "日"};
    private static final int HEART_RED = Color.rgb(224, 64, 64);
    private static final int HEART_SOFT = Color.rgb(252, 230, 228);
    private static final String SEARCH_PROVIDER_GROQ = "groq";
    private static final String SEARCH_PROVIDER_GEMINI = "gemini";

    private final List<Exercise> seedExercises = SeedExercises.defaultExercises();
    private final List<Exercise> datasetExercises = new ArrayList<Exercise>();
    private final List<Exercise> customExercises = new ArrayList<Exercise>();
    private final List<PendingShare> pendingShares = new ArrayList<PendingShare>();
    private final List<SessionRecord> trainingRecords = new ArrayList<SessionRecord>();
    private final List<Recipe> recipes = new ArrayList<Recipe>();
    private final Set<String> favoriteIds = new HashSet<String>();
    private final Set<String> verifiedIds = new HashSet<String>();
    private final Set<String> deletedExerciseIds = new HashSet<String>();
    private final Set<String> deletedCategories = new HashSet<String>();
    private final Set<String> equipment = new LinkedHashSet<String>();
    private final Map<String, String> mediaOverrides = new HashMap<String, String>();
    /** 最近生成但未必已经完成的动作；用于连续“重新安排”时在同类动作内轮换。 */
    private final List<String> recentRecommendationIds = new ArrayList<String>();
    private final Map<String, Bitmap> thumbCache = new HashMap<String, Bitmap>();
    private Bitmap regionSpriteBitmap;
    private static final int REQ_PICK_MEDIA = 4201;
    private static final int REQ_EXPORT_BACKUP = 4202;
    private static final int REQ_IMPORT_BACKUP = 4203;
    private static final int REQ_HEALTH_PERMISSION = 4204;
    private static final int REQ_PICK_RECIPE_IMPORT = 4205;
    private static final int REQ_PICK_RECIPE_PHOTO = 4206;
    private static final int REQ_PICK_RECIPE_COVER = 4207;
    private static final int REQ_PICK_STEP_IMAGE = 4208;
    private static final int REQ_PICK_MEAL_PHOTO = 4209;
    private static final int REQ_UPDATE_INSTALL_PERMISSION = 4210;
    private static final String HEALTH_READ_HEART_RATE = "android.permission.health.READ_HEART_RATE";
    /** 读手表自己的运动记录，用来把统计窗口对齐到它的起止时刻。 */
    private static final String HEALTH_READ_EXERCISE = "android.permission.health.READ_EXERCISE";
    private static final String[] HEALTH_PERMISSIONS = {HEALTH_READ_HEART_RATE, HEALTH_READ_EXERCISE,
            WatchMetricsReader.ACTIVE, WatchMetricsReader.TOTAL, WatchMetricsReader.STEPS, WatchMetricsReader.DISTANCE};

    /** 找手表运动记录时向两边多看的范围。 */
    private static final long SESSION_MATCH_SLACK_MS = 30 * 60 * 1000L;
    /** 至少要重叠这么久才认为是同一次训练。 */
    private static final long MIN_SESSION_OVERLAP_MS = 3 * 60 * 1000L;
    /** 查询心率时多留的余量，容忍手机和手表的时钟偏差；统计仍只取窗口内。 */
    private static final long HR_QUERY_SLACK_MS = 90 * 1000L;
    /** 超过一天还没同步上就不再自动重试。 */
    private static final long HR_RETRY_WINDOW_MS = 24 * 60 * 60 * 1000L;
    private static final int MAX_HR_RETRIES_PER_RESUME = 3;

    /** 发给 AI 的每个槽位候选数：够它挑，又不至于把 prompt 撑爆。 */
    private static final int AI_CANDIDATES_PER_SLOT = 8;

    /** 常见手表配套 App 的包名，用来在记录上标出心率来源。 */
    private static final Map<String, String> KNOWN_HEALTH_APPS = knownHealthApps();

    private static Map<String, String> knownHealthApps() {
        Map<String, String> map = new HashMap<String, String>();
        map.put("com.mi.health", "小米运动健康");
        map.put("com.xiaomi.wearable", "小米穿戴");
        map.put("com.huawei.health", "华为运动健康");
        map.put("com.garmin.android.apps.connectmobile", "佳明 Connect");
        map.put("com.samsung.android.app.shealth", "三星健康");
        map.put("com.google.android.apps.fitness", "Google Fit");
        map.put("com.fitbit.FitbitMobile", "Fitbit");
        map.put("com.amazfit.watch", "Zepp");
        map.put("com.huami.watch.hmwatchmanager", "Zepp");
        return Collections.unmodifiableMap(map);
    }

    private EditText pendingMediaField;
    private String pendingHeartRateRecordKey;
    private String pendingRecipePhotoId;
    private int pendingStepIndex = -1;

    // Guided training session state
    private boolean inSession;
    private int sessionIndex;
    private boolean exerciseRunning;
    private final WorkoutClock workoutClock = new WorkoutClock();
    private long sessionStartEpochMillis;
    private long exerciseStartedActiveMillis;
    private final List<String> sessionResults = new ArrayList<String>();
    /** 与 sessionResults 平行的结构化结果 "动作id|组数|是否完成"。 */
    private final List<String> sessionStats = new ArrayList<String>();
    private int sessionSetIndex;
    private boolean inRest;

    // —— 引导式训练的节拍与语音 ——
    /** 倒数几秒进入下一组。 */
    private static final int COUNT_IN_SECONDS = 3;
    /** 剩几秒开始报数。 */
    private static final int VOICE_COUNTDOWN_FROM = 10;
    private static final long TICK_INTERVAL_MILLIS = 200L;

    private SessionPhase sessionPhase = SessionPhase.PREPARE;
    private boolean sessionVisible;
    private int quickMinutes = 8;
    private boolean quickGentle = false;
    private Intensity defaultIntensity = Intensity.MEDIUM;
    private Intensity quickIntensityOverride = null;
    private Intensity customIntensityOverride = null;
    private String trainingPage = "home";
    private String commandDraft = "";
    private int planGeneration;
    private int planBudgetMinutes;
    private boolean sessionHadPause;
    private Chronometer sessionChronometer;
    private Chronometer setChronometer;
    private long lastCheckpointRealtime;
    private int lastSpokenSecond = -1;
    private boolean switchSideSpoken;
    private TextView countdownLabel;
    private final Handler sessionTicker = new Handler(Looper.getMainLooper());
    private final Runnable tickRunnable = this::onTick;
    private final VoiceCues voiceCues = new VoiceCues(this);

    private LinearLayout root;
    private LinearLayout content;
    private LinearLayout bottomNav;
    private ScrollView mainScrollView;
    private EditText commandInput;
    private TextView statusLine;
    private Intensity selectedIntensity = Intensity.MEDIUM;
    private int selectedDurationMinutes = 25;
    private PainSeverity shoulderPain;
    private PainSeverity lowerBackPain;
    private PainSeverity kneePain;
    private String currentTab = "training";
    private String libraryFilter = "全部";
    private String libraryQuery = "";
    private String libraryReviewFilter = "全部状态";
    private boolean reviewedOnly;
    private ExerciseReviewStore exerciseReviews;
    private int libraryVisibleLimit = 60;
    private String datasetLoadError = "";
    private String foodPreferenceText = "";
    private EditText foodPreferenceInput;
    private String recommendedRecipeId;
    private String recommendedRecipeReason = "";
    private Recipe recommendedWebRecipe;
    private boolean lastRecommendRandom;
    private final Random random = new Random();

    // Recipe detail / editor page state (full-page, 下厨房-style)
    private String currentRecipeId;
    private Recipe editorDraft;
    private boolean editorIsNew;
    private EditText edRecipeName;
    private EditText edRecipeReview;
    private EditText edRecipeTags;
    private final List<EditText> edIngredientFields = new ArrayList<EditText>();
    private final List<EditText> edStepFields = new ArrayList<EditText>();

    // AI recommendation (opt-in, uses the user's own free Gemini key; falls back to local logic)
    private boolean aiEnabled;
    private String aiApiKey = "";
    private String aiModel = GeminiModelName.DEFAULT_MODEL;
    private String aiSearchApiKey = "";
    private String aiSearchProvider = SEARCH_PROVIDER_GROQ;
    private String aiSearchEndpoint = GroqEndpoint.DEFAULT_ENDPOINT;
    private String aiSearchModel = GroqEndpoint.DEFAULT_MODEL;
    private boolean aiThinking;
    private boolean currentPlanFromAi;
    private final GeminiClient geminiClient = new GeminiClient();
    private final GroqClient groqClient = new GroqClient();
    private final GitHubUpdater githubUpdater = new GitHubUpdater();
    private String githubUpdateStatus = "尚未检查更新";
    private boolean githubUpdateBusy;
    private TextView githubUpdateStatusView;
    private Button githubUpdateButton;
    private File pendingUpdateApk;
    private WorkoutPlan currentPlan;
    private RecommendationInput lastInput;
    private final List<WorkoutItem> activeItems = new ArrayList<WorkoutItem>();

    // —— 周期计划与状态评估 ——
    private AssessmentResult assessment;
    /** 新版保存原始问卷，设置页“修改评估”才能准确回填；旧版记录为 null。 */
    private AssessmentInput assessmentInput;
    private String assessmentDate = "";
    private TrainingProgram program;
    /** 绑日期的训练日历：动作在生成计划时就排好，漏练标记 MISSED 而不是顺延。 */
    private ProgramSchedule schedule;
    private final List<Integer> programWeekdays = new ArrayList<Integer>();
    private String pendingProgramKey = "";      // 正在练的那次日历安排的 key
    private long calendarAnchorEpochDay;        // 日历当前显示的月份
    private boolean programUseAi = true;        // 生成计划时让 AI 参与挑动作
    /** 个人化的节奏系数：用每次训练的「预计 vs 实际」滚动校准，让时长估算贴合本人。 */
    private double paceFactor = 1.0;
    /** 训练时的语音口令开关。 */
    private boolean voiceEnabled = true;

    // —— 营养目标与今日记录 ——
    private NutritionProfile nutritionProfile;
    private EnergyPlan energyPlan;
    private PagodaTargets pagodaTargets;
    private final List<BuiltinRecipe> builtinRecipes = new ArrayList<BuiltinRecipe>();
    private final Map<String, DayFoodLog> foodLogs = new HashMap<String, DayFoodLog>();
    private String scienceRecId = "";
    private String scienceRecReason = "";
    private String scienceSlot = "";
    private String recipeFilter = "all";   // 菜谱库列表：all / mine / science
    /** 今日饮食默认只露出摘要，需要微调克数时再展开，避免把推荐区推到数屏之外。 */
    private boolean foodLogExpanded;
    // 「记一餐」：预设是只读数据，草稿是本次未确认的选择，不进 saveState。
    private final List<MealPreset> mealPresets = new ArrayList<MealPreset>();
    private final MealDraft mealDraft = new MealDraft();
    private EditText mealEstimateInput;
    private String mealEstimateText = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        loadBundledExerciseDataset();
        builtinRecipes.addAll(BuiltinRecipeLoader.load(this));
        mealPresets.addAll(QuickMealLoader.load(this));
        equipment.addAll(Arrays.asList("自重", "弹力带", "哑铃", "固定器械", "高位下拉器"));
        loadState();
        exerciseReviews = new ExerciseReviewStore(this);
        exerciseReviews.load(datasetExercises, getSharedPreferences("fitness_state", MODE_PRIVATE)
                .getString("exerciseReviewsV1", "{}"));
        restoreWorkoutDraft();
        rebuildNutritionDerived();
        if (handleIncomingShare(getIntent())) {
            saveState();
        }
        buildRoot();
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
                    android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::handleBackNavigation);
        }
        renderTraining();
        String action = getIntent() == null ? null : getIntent().getAction();
        if ("androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE".equals(action)
                || Intent.ACTION_VIEW_PERMISSION_USAGE.equals(action)) {
            new AlertDialog.Builder(this)
                    .setTitle("心率数据用途")
                    .setMessage("本 App 只读取手表写入健康连接的心率，用于归档到对应的训练记录；数据只保存在本机，不会上传。")
                    .setPositiveButton("知道了", null)
                    .show();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (inSession && sessionVisible) renderSession();
        // 手表配套 App 往往训练结束后几分钟才把数据推到健康连接，所以每次回到 App 补一次同步。
        retryPendingHeartRateSyncs();
        if (refreshScheduleStatus()) {
            saveState();
            if ("training".equals(currentTab) && !inSession) {
                renderTraining();
            }
        }
    }

    @Override
    protected void onPause() {
        pauseWorkout();
        stopTicker();
        voiceCues.end();
        saveState();
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        stopTicker();
        voiceCues.release();
        githubUpdater.cancel();
        super.onDestroy();
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        if (handleIncomingShare(intent)) {
            pauseWorkout();
            saveState();
            Toast.makeText(this, "已加入待确认动作", Toast.LENGTH_SHORT).show();
            renderLibrary("待确认");
        }
    }

    private void buildRoot() {
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackground(new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,
                new int[]{Color.rgb(237, 243, 238), BG, Color.rgb(244, 246, 240)}));

        mainScrollView = new ScrollView(this);
        mainScrollView.setFillViewport(true);
        mainScrollView.setClipToPadding(false);
        mainScrollView.setClipChildren(false);
        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setClipToPadding(false);
        content.setClipChildren(false);
        content.setPadding(dp(18), dp(18), dp(18), dp(22));
        mainScrollView.addView(content, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        root.addView(mainScrollView, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        View divider = new View(this);
        divider.setBackgroundColor(Color.rgb(232, 236, 229));
        root.addView(divider, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, Math.max(1, dp(1) / 2 + 1)));

        bottomNav = new LinearLayout(this);
        bottomNav.setOrientation(LinearLayout.HORIZONTAL);
        bottomNav.setPadding(dp(8), dp(8), dp(8), dp(8));
        bottomNav.setBackgroundColor(SURFACE);
        root.addView(bottomNav, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        root.setOnApplyWindowInsetsListener((view, insets) -> {
            content.setPadding(dp(18), dp(18) + insets.getSystemWindowInsetTop(), dp(18), dp(22));
            bottomNav.setPadding(dp(8), dp(8), dp(8), dp(8) + insets.getSystemWindowInsetBottom());
            return insets;
        });

        setContentView(root);
    }

    private boolean handleIncomingShare(Intent intent) {
        if (intent == null || !Intent.ACTION_SEND.equals(intent.getAction())) {
            return false;
        }
        String title = stringExtra(intent, Intent.EXTRA_SUBJECT);
        String body = stringExtra(intent, Intent.EXTRA_TEXT);
        Uri stream = intent.getParcelableExtra(Intent.EXTRA_STREAM);
        String uri = stream == null ? "" : stream.toString();
        if (title.length() == 0 && body.length() == 0 && uri.length() == 0) {
            return false;
        }
        pendingShares.add(new PendingShare(
                title.length() == 0 ? "外部保存动作" : title,
                body,
                uri,
                new SimpleDateFormat("MM-dd HH:mm", Locale.CHINA).format(new Date())));
        return true;
    }

    private String stringExtra(Intent intent, String key) {
        CharSequence value = intent.getCharSequenceExtra(key);
        return value == null ? "" : value.toString();
    }

    /** A single next step, followed by actual history. Configuration lives one level deeper. */
    private void renderTraining() {
        currentTab = "training";
        clear();
        trainingPage = "home";
        content.addView(title("时光屋", new SimpleDateFormat("M月d日 EEEE", Locale.CHINA).format(new Date())));
        content.addView(text("给自己一点时间", 28, Typeface.BOLD, INK));
        content.addView(text("从今天能做到的开始。", 14, Typeface.NORMAL, MUTED));
        content.addView(reviewScopeButton(this::renderTraining), fullButton());
        content.addView(space(12));

        LinearLayout hero = card();
        hero.setPadding(dp(22), dp(22), dp(22), dp(20));
        hero.setBackground(bg(Color.rgb(27, 66, 55), dp(24), GREEN, 0));
        final ScheduledSession today = nextSessionToday();
        if (inSession) {
            hero.addView(text("进度已保留", 12, Typeface.BOLD, Color.rgb(190, 221, 202)));
            hero.addView(space(10));
            hero.addView(text("接着上次，慢慢来", 25, Typeface.BOLD, Color.WHITE));
            hero.addView(space(8));
            hero.addView(text(activeItems.get(sessionIndex).exercise().name() + " · 第 "
                    + (sessionSetIndex + 1) + " 组", 15, Typeface.NORMAL, Color.WHITE));
            hero.addView(text("已练 " + formatDuration(workoutClock.elapsed(SystemClock.elapsedRealtime()) / 1000)
                    + " · 暂停期间不计时", 13, Typeface.NORMAL, Color.rgb(200, 224, 210)));
            hero.addView(space(18));
            hero.addView(button("回到训练 →", Color.rgb(218, 241, 177), INK, v -> renderSession()), fullButton());
        } else if (currentPlan != null && !activeItems.isEmpty()) {
            hero.addView(text("你的课程已备好", 12, Typeface.BOLD, Color.rgb(190, 221, 202)));
            hero.addView(space(10));
            hero.addView(text("准备好了，就开始", 25, Typeface.BOLD, Color.WHITE));
            hero.addView(space(8));
            hero.addView(text(activeItems.size() + " 个动作 · 主课约 " + timeModel().sessionMinutes(activeItems)
                    + " 分钟", 15, Typeface.NORMAL, Color.WHITE));
            hero.addView(space(18));
            hero.addView(button("查看课程 →", Color.rgb(218, 241, 177), INK, v -> renderWorkoutPreview()), fullButton());
            hero.addView(button("重新安排", Color.TRANSPARENT, Color.WHITE, v -> {
                currentPlan = null;
                activeItems.clear();
                pendingProgramKey = "";
                persistWorkoutDraft();
                renderTraining();
            }), fullButton());
        } else if (today != null) {
            List<WorkoutItem> items = scheduledItems(today, program.phaseForWeek(today.week()));
            hero.addView(text("今天的计划", 12, Typeface.BOLD, Color.rgb(190, 221, 202)));
            hero.addView(space(10));
            hero.addView(text(today.focus().label(), 28, Typeface.BOLD, Color.WHITE));
            hero.addView(space(8));
            hero.addView(text("第 " + today.week() + " 周 · " + items.size() + " 个动作 · 主课约 "
                    + timeModel().sessionMinutes(items) + " 分钟", 14, Typeface.NORMAL, Color.WHITE));
            hero.addView(space(18));
            hero.addView(button("查看今日课程 →", Color.rgb(218, 241, 177), INK,
                    v -> startScheduledSession(today)), fullButton());
            hero.addView(button("今天只想短练一下", Color.TRANSPARENT, Color.WHITE,
                    v -> generateQuickWorkout()), fullButton());
        } else {
            hero.addView(text("今天，从一小步开始", 12, Typeface.BOLD, Color.rgb(190, 221, 202)));
            hero.addView(space(8));
            LinearLayout heading = new LinearLayout(this);
            heading.setGravity(Gravity.CENTER_VERTICAL);
            TextView minutes = text(String.valueOf(quickMinutes), 62, Typeface.BOLD, Color.WHITE);
            heading.addView(minutes);
            TextView unit = text("  分钟\n  主课时间预算", 13, Typeface.NORMAL, Color.rgb(200, 224, 210));
            heading.addView(unit);
            hero.addView(heading);
            hero.addView(text(quickGentle ? "轻轻练，也算认真对待自己。" : "留一段时间，专心动一动。",
                    15, Typeface.NORMAL, Color.WHITE));
            hero.addView(space(14));
            LinearLayout times = new LinearLayout(this);
            int[] budgets = {8, 15, 25};
            for (int i = 0; i < budgets.length; i++) {
                final int budget = budgets[i];
                Button choice = button(budget + " 分钟", budget == quickMinutes ? Color.WHITE : Color.rgb(47, 84, 70),
                        budget == quickMinutes ? INK : Color.WHITE, v -> {
                            quickMinutes = budget;
                            saveState();
                            renderTraining();
                        });
                choice.setSingleLine(true);
                choice.setTextSize(13);
                choice.setMinWidth(0);
                choice.setSelected(budget == quickMinutes);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(0, dp(46), 1);
                lp.setMargins(i == 0 ? 0 : dp(4), 0, i == budgets.length - 1 ? 0 : dp(4), 0);
                times.addView(choice, lp);
            }
            hero.addView(times);
            hero.addView(space(10));
            Button intensityToggle = button(quickGentle ? "轻松模式 · 点此切换为日常强度" : "日常强度 · 点此切换为轻松模式",
                    Color.TRANSPARENT, Color.rgb(211, 233, 220), v -> {
                        quickGentle = !quickGentle;
                        quickIntensityOverride = quickGentle ? Intensity.LOW : Intensity.MEDIUM;
                        saveState();
                        renderTraining();
                    });
            intensityToggle.setSingleLine(true);
            intensityToggle.setTextSize(13);
            hero.addView(intensityToggle, fullButton());
            hero.addView(text(quickIntensityOverride == null
                    ? "本次跟随默认：" + defaultIntensity.label() + "强度"
                    : "本次已手动选择：" + quickIntensityOverride.label() + "强度", 12, Typeface.NORMAL, Color.WHITE));
            if (quickIntensityOverride != null) hero.addView(button("恢复跟随默认强度", Color.TRANSPARENT,
                    Color.WHITE, v -> {
                        quickIntensityOverride = null;
                        quickGentle = defaultIntensity == Intensity.LOW;
                        saveState(); renderTraining();
                    }), fullButton());
            hero.addView(space(4));
            hero.addView(button("为我安排这一练 →", Color.rgb(218, 241, 177), INK,
                    v -> generateQuickWorkout()), fullButton());
            hero.addView(space(8));
            hero.addView(text("按当前器械与伤痛设置安排 · 无需联网", 11, Typeface.NORMAL, Color.rgb(200, 224, 210)));
        }
        content.addView(hero);
        content.addView(button("我的动作组 · 保存组合直接练", SURFACE, GREEN, v -> renderRoutines()), fullButton());
        content.addView(weekFootprintCard());
        if (!inSession) {
            LinearLayout links = new LinearLayout(this);
            links.addView(button("自己安排", SURFACE, GREEN, v -> renderAdHocSetup()),
                    new LinearLayout.LayoutParams(0, dp(52), 1));
            links.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
            links.addView(button(program == null ? "建立周期计划" : "训练日历", SURFACE, GREEN, v -> {
                if (program == null) {
                    if (assessment == null) renderAssessmentForm(); else renderProgramSetup();
                } else renderCalendar();
            }), new LinearLayout.LayoutParams(0, dp(52), 1));
            content.addView(links);
        }
        renderBottomNav();
        scrollToTop();
    }

    private ScheduledSession nextSessionToday() {
        if (schedule == null || program == null) return null;
        for (ScheduledSession s : schedule.onDate(todayEpochDay())) {
            if (s.status() == ScheduledSession.Status.PLANNED) return s;
        }
        return null;
    }

    private LinearLayout.LayoutParams fullButton() {
        return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private void scrollToTop() {
        content.setFocusableInTouchMode(true);
        content.requestFocus();
        mainScrollView.post(() -> mainScrollView.scrollTo(0, 0));
    }

    private int recordedSets(SessionRecord record) {
        int total = 0;
        for (String stat : record.itemStats) {
            String[] parts = stat.split("\\|");
            if (parts.length > 1) {
                try { total += Math.max(0, Integer.parseInt(parts[1])); }
                catch (NumberFormatException ignored) { }
            }
        }
        return total;
    }

    private View weekFootprintCard() {
        long start = ProgramSchedule.startOfWeek(todayEpochDay());
        Set<Long> days = new HashSet<Long>();
        int sets = 0;
        for (SessionRecord record : trainingRecords) {
            if (record.epochMillis <= 0 || (recordedSets(record) == 0 && record.done == 0)) continue;
            long day = Instant.ofEpochMilli(record.epochMillis).atZone(java.time.ZoneId.systemDefault()).toLocalDate().toEpochDay();
            if (day >= start && day <= todayEpochDay()) {
                days.add(day);
                sets += recordedSets(record);
            }
        }
        LinearLayout card = card();
        card.setElevation(0);
        card.addView(text("这一周的足迹", 17, Typeface.BOLD, INK));
        card.addView(space(12));
        LinearLayout week = new LinearLayout(this);
        for (int i = 0; i < 7; i++) {
            long day = start + i;
            LinearLayout cell = new LinearLayout(this);
            cell.setOrientation(LinearLayout.VERTICAL);
            cell.setGravity(Gravity.CENTER);
            cell.addView(text(WEEKDAY_SHORT[i], 12, Typeface.NORMAL, MUTED));
            cell.addView(space(6));
            TextView dot = text(days.contains(day) ? "✓" : String.valueOf(LocalDate.ofEpochDay(day).getDayOfMonth()),
                    14, Typeface.BOLD, days.contains(day) ? Color.WHITE : INK);
            dot.setGravity(Gravity.CENTER);
            dot.setBackground(bg(days.contains(day) ? GREEN : BG, dp(20),
                    day == todayEpochDay() ? GREEN : BG, day == todayEpochDay() ? 2 : 0));
            dot.setContentDescription(dateLabel(day) + (days.contains(day) ? " 已训练" : " 暂无训练记录"));
            cell.addView(dot, new LinearLayout.LayoutParams(dp(34), dp(34)));
            week.addView(cell, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        }
        card.addView(week);
        card.addView(space(12));
        card.addView(text(days.isEmpty() ? "还没有足迹。今天的一小步，会留在这里。"
                : "本周动了 " + days.size() + " 天" + (sets > 0 ? " · 完成 " + sets + " 组，每一组都算数。"
                : "，每一次都算数。"), 13, Typeface.NORMAL, MUTED));
        card.setOnClickListener(v -> renderRecords());
        return card;
    }

    private Intensity allowedDailyIntensity(Intensity requested) {
        if ((assessment != null && assessment.medicalClearanceAdvised())
                || shoulderPain == PainSeverity.SEVERE || lowerBackPain == PainSeverity.SEVERE
                || kneePain == PainSeverity.SEVERE) return Intensity.LOW;
        return requested;
    }

    private WorkoutPlan explainDailyIntensity(WorkoutPlan plan, Intensity requested) {
        List<String> notes = new ArrayList<>(plan.avoidanceNotes());
        boolean limited = plan.intensity() != requested && allowedDailyIntensity(requested) != requested;
        String limitReason = "";
        if (limited) {
            List<String> reasons = new ArrayList<>();
            if (shoulderPain == PainSeverity.SEVERE) reasons.add("肩部伤痛设为急性");
            if (lowerBackPain == PainSeverity.SEVERE) reasons.add("腰部伤痛设为急性");
            if (kneePain == PainSeverity.SEVERE) reasons.add("膝部伤痛设为急性");
            if (assessment != null && assessment.medicalClearanceAdvised())
                reasons.add((assessmentDate.length() > 0 ? assessmentDate + " 的" : "已保存的") + "体能评估存在安全筛查阳性项");
            limitReason = "本次选择" + requested.label() + "强度；因" + join(reasons)
                    + "，实际按低强度安排。可到设置核对伤痛或重新进行体能评估。";
            notes.add(limitReason);
        }
        Set<String> used = new LinkedHashSet<>();
        for (WorkoutItem item : plan.items()) used.addAll(item.exercise().equipment());
        notes.add("本次使用：" + join(new ArrayList<>(used)) + "。器械按动作结构选用，不要求每节课用完全部器械。");
        String effort = plan.intensity() == Intensity.LOW ? "轻松强度：优先控制动作，保留明显余力。"
                : "日常强度：主动作目标 RPE 7–8，约还可完成 2–3 次；用重量、支撑角度调节难度。完成上限次数且明显偏轻，下次小幅增加负重或难度。";
        return new WorkoutPlan((limited ? "已降为轻松 · " : "") + plan.title(), plan.intensity(), plan.estimatedMinutes(), plan.items(),
                effort + plan.recommendationReason(), notes, limited ? limitReason : plan.safetyMessage(), limited || plan.isSafetyLimited());
    }

    private void generateQuickWorkout() {
        if (inSession) { renderSession(); return; }
        planGeneration++;
        planBudgetMinutes = quickMinutes;
        Intensity requestedIntensity = quickIntensityOverride == null ? defaultIntensity : quickIntensityOverride;
        Intensity effectiveIntensity = allowedDailyIntensity(requestedIntensity);
        String intentText = requestedIntensity == Intensity.LOW ? "轻松恢复" : "";
        AdHocIntent intent = AdHocIntent.parse(intentText);
        lastInput = adHocInput(intentText, intentText.isEmpty(), intent, effectiveIntensity);
        WorkoutPlan plan = AdHocPlanner.plan(engine().safeCandidates(lastInput), new AdHocPlanner.Request()
                .intent(intent).minutes(quickMinutes).intensity(effectiveIntensity).level(currentLevel())
                .paceFactor(paceFactor).recovery(recoveryState()).ledger(weeklyLedger())
                .tomorrowRegions(tomorrowPlannedRegions()).favoriteIds(favoriteIds)
                .recentExerciseIds(recentExerciseIdsForRecommendation()));
        pendingProgramKey = "";
        applyGeneratedPlan(explainDailyIntensity(plan, requestedIntensity), false);
    }

    private String workoutItemLabel(WorkoutItem item) {
        Prescription p = item.prescription();
        String label = p.compactLabel().replace(" · 休息 " + p.restSeconds() + " 秒", "");
        if (p.sets() > 1) label += " · 组间休息 " + p.restSeconds() + " 秒";
        if (item.restAfterSeconds() > 0) label += " · 动作后休息 " + item.restAfterSeconds() + " 秒";
        if (!item.weight().isEmpty()) label += " · 重量 " + item.weight();
        return reviewLabel(item.exercise()) + " · " + label;
    }

    private void renderWorkoutPreview() {
        if (inSession) { renderSession(); return; }
        if (currentPlan == null) { renderTraining(); return; }
        currentTab = "training";
        clear();
        trainingPage = "preview";
        content.addView(title("这一练", "已按你的设置安排，准备好就开始"));
        content.addView(button("‹ 回到今天", GREEN_SOFT, GREEN, v -> renderTraining()), fullButton());
        LinearLayout intro = card();
        intro.addView(text(currentPlan.title(), 22, Typeface.BOLD, INK));
        intro.addView(space(8));
        intro.addView(text("主课约 " + timeModel().sessionMinutes(activeItems) + " 分钟 · " + activeItems.size() + " 个动作",
                16, Typeface.BOLD, GREEN));
        intro.addView(text("另留热身 " + SessionTimeModel.WARMUP_ADVICE_MINUTES + " 分钟、放松 "
                + SessionTimeModel.COOLDOWN_ADVICE_MINUTES + " 分钟", 13, Typeface.NORMAL, MUTED));
        intro.addView(space(12));
        if (!activeItems.isEmpty()) intro.addView(button("开始这一练 →", GREEN, Color.WHITE, v -> startSession()), fullButton());
        intro.addView(space(8));
        intro.addView(text(currentPlan.safetyMessage(), 12, Typeface.NORMAL,
                currentPlan.isSafetyLimited() ? CORAL : MUTED));
        if (activeItems.isEmpty()) {
            intro.addView(text("当前复核范围、器械和伤痛条件下没有可用动作。请调整器械，或先复核适合的动作。", 14, Typeface.NORMAL, MUTED));
            intro.addView(button("查看设置", GREEN_SOFT, GREEN, v -> renderSettings()), fullButton());
        }
        content.addView(intro);
        if (!activeItems.isEmpty() && activeItems.size() <= 30) content.addView(button("存为我的动作组", GREEN_SOFT, GREEN, v ->
                editRoutine(new WorkoutRoutine(java.util.UUID.randomUUID().toString(), currentPlan.title(), "", false, 1, 0, activeItems))), fullButton());
        for (int i = 0; i < activeItems.size(); i++) {
            final int index = i;
            WorkoutItem item = activeItems.get(i);
            LinearLayout row = card();
            row.setElevation(0);
            row.addView(text(String.format(Locale.CHINA, "%02d  %s", i + 1, item.exercise().name()), 18, Typeface.BOLD, INK));
            row.addView(space(4));
            row.addView(text(workoutItemLabel(item), 13, Typeface.NORMAL, MUTED));
            row.addView(text(item.reason(), 12, Typeface.NORMAL, GREEN));
            LinearLayout actions = new LinearLayout(this);
            actions.addView(button("看示范与要点", GREEN_SOFT, GREEN, v -> showExerciseDetail(item.exercise())),
                    new LinearLayout.LayoutParams(0, dp(48), 2));
            actions.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
            if (lastInput != null && pendingProgramKey.isEmpty()) actions.addView(button("换一个", BG, INK, v -> replaceItem(index)),
                    new LinearLayout.LayoutParams(0, dp(48), 1));
            row.addView(space(8));
            row.addView(actions);
            row.addView(button("调整组数、次数、休息与重量", BG, GREEN, v -> editActiveItem(index)), fullButton());
            content.addView(row);
        }
        LinearLayout why = card();
        why.addView(text("安排说明", 15, Typeface.BOLD, INK));
        why.addView(text(currentPlan.recommendationReason(), 13, Typeface.NORMAL, MUTED));
        for (String note : currentPlan.avoidanceNotes()) why.addView(text("· " + note, 13, Typeface.NORMAL, MUTED));
        content.addView(why);
        renderBottomNav();
        scrollToTop();
    }

    private void renderAdHocSetup() {
        currentTab = "training";
        clear();
        trainingPage = "custom";
        content.addView(title("自己安排", "按部位、时间和今天的状态来练"));
        content.addView(reviewScopeButton(this::renderAdHocSetup), fullButton());
        content.addView(button("‹ 回到今天", GREEN_SOFT, GREEN, v -> renderTraining()));
        content.addView(button("编排并保存动作组", GREEN_SOFT, GREEN, v -> renderRoutines()), fullButton());
        content.addView(statusCard());
        content.addView(space(10));

        LinearLayout commandCard = card();
        commandInput = new EditText(this);
        commandInput.setSingleLine(false);
        commandInput.setMinLines(2);
        commandInput.setHint("今天想练什么？比如：我想练背，但腰有点不舒服");
        commandInput.setText(commandDraft);
        commandInput.setTextColor(INK);
        commandInput.setHintTextColor(Color.rgb(126, 137, 132));
        commandInput.setTextSize(16);
        commandInput.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        commandInput.setBackground(bg(Color.rgb(249, 251, 247), dp(8), LINE, 1));
        commandInput.setPadding(dp(12), dp(10), dp(12), dp(10));
        commandCard.addView(section("临时加练"));
        commandCard.addView(space(4));
        commandCard.addView(text("说说想练哪里，也可以直接选一个部位。", 13, Typeface.NORMAL, MUTED));
        commandCard.addView(space(8));
        commandCard.addView(commandInput, matchWrap());
        commandCard.addView(space(10));
        commandCard.addView(intensityRow());
        commandCard.addView(text(customIntensityOverride == null ? "本次跟随默认强度" : "本次已手动选择强度", 12, Typeface.NORMAL, MUTED));
        if (customIntensityOverride != null) commandCard.addView(button("恢复跟随默认强度", GREEN_SOFT, GREEN, v -> {
            commandDraft = commandInput.getText().toString();
            customIntensityOverride = null; selectedIntensity = defaultIntensity;
            saveState(); renderAdHocSetup();
        }));
        commandCard.addView(space(6));
        commandCard.addView(durationRow());
        commandCard.addView(space(10));
        commandCard.addView(quickRow(new String[]{"练背", "练腿", "练胸", "全身", "恢复"}));
        commandCard.addView(space(6));
        String recovering = recoveringHint();
        if (recovering.length() > 0) {
            commandCard.addView(text(recovering, 12, Typeface.NORMAL, CORAL));
            commandCard.addView(space(6));
        }
        commandCard.addView(space(6));

        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        actions.addView(button("生成加练", GREEN, Color.WHITE, v -> generateFromCommand(false)),
                new LinearLayout.LayoutParams(0, dp(46), 1f));
        actions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        actions.addView(button("不知道练什么", BLUE, Color.WHITE, v -> generateFromCommand(true)),
                new LinearLayout.LayoutParams(0, dp(46), 1f));
        commandCard.addView(actions);
        content.addView(commandCard);

        View volumeCard = weeklyVolumeCard();
        if (volumeCard != null) {
            content.addView(space(10));
            content.addView(volumeCard);
        }

        if (aiThinking) {
            content.addView(aiThinkingCard("AI 正在结合你的目标和伤痛设置安排训练…"));
        }

        renderBottomNav();
    }

    /** 还在恢复窗口里的部位 + 明天计划课要练的部位，提前告诉用户加练会避开什么。 */
    private String recoveringHint() {
        List<String> parts = new ArrayList<String>();
        RecoveryState recovery = recoveryState();
        List<String> recovering = recovery.recoveringRegions();
        if (!recovering.isEmpty()) {
            parts.add("48 小时内练过：" + join(recovering));
        }
        Set<String> tomorrow = tomorrowPlannedRegions();
        if (!tomorrow.isEmpty()) {
            parts.add("明天计划练：" + join(new ArrayList<String>(tomorrow)));
        }
        if (parts.isEmpty()) {
            return "";
        }
        return "会自动避开 —— " + join(parts);
    }

    private View aiThinkingCard(String label) {
        LinearLayout card = card();
        card.addView(smallLabel("AI 推荐"));
        card.addView(space(6));
        card.addView(text(label, 15, Typeface.BOLD, INK));
        card.addView(space(4));
        card.addView(text("如果网络较慢或额度用尽，会自动切回本地推荐。", 13, Typeface.NORMAL, MUTED));
        return card;
    }

    private View statusCard() {
        LinearLayout card = card();
        card.addView(smallLabel("当前状态"));
        statusLine = text(selectedIntensity.label() + "强度 · " + durationLabel(selectedDurationMinutes) + " · 器械 " + equipment.size()
                + " 项 · 伤痛：" + painSummary(), 15, Typeface.BOLD, INK);
        card.addView(statusLine);
        card.addView(space(6));
        card.addView(text("默认避开急性/明显伤痛冲突动作；未验证动作不会自动进入推荐。", 13, Typeface.NORMAL, MUTED));
        return card;
    }

    private View emptyTrainingCard() {
        LinearLayout card = card();
        card.addView(section("今日推荐"));
        card.addView(text("输入目标或直接点“不知道练什么”，这里会生成动作、组数、次数、RPE、休息和避让说明。", 14, Typeface.NORMAL, MUTED));
        if (!trainingRecords.isEmpty()) {
            card.addView(space(10));
            card.addView(smallLabel("最近训练"));
            card.addView(text(trainingRecords.get(0).summary(), 14, Typeface.NORMAL, INK));
        }
        if (!pendingShares.isEmpty()) {
            card.addView(space(10));
            card.addView(text("待确认动作：" + pendingShares.size() + " 个", 14, Typeface.BOLD, CORAL));
        }
        return card;
    }

    /**
     * 临时加练入口。走 {@link AdHocPlanner} 而不是计划课那条线——
     * 这里时长是硬约束、组数是解出来的，还要避开刚练过的部位和明天计划课要练的部位。
     */
    private void generateFromCommand(boolean unknown) {
        String text = unknown ? "" : commandInput.getText().toString();
        commandDraft = text;
        generateAdHocSession(text, unknown);
    }

    private void applyPlan(WorkoutPlan plan, boolean fromAi) {
        aiThinking = false;
        if (inSession) return;
        currentPlan = plan;
        currentPlanFromAi = fromAi;
        activeItems.clear();
        activeItems.addAll(plan.items());
        persistWorkoutDraft();
        if ("training".equals(currentTab) && !inSession) {
            renderWorkoutPreview();
        }
    }

    private void applyGeneratedPlan(WorkoutPlan plan, boolean fromAi) {
        rememberRecommendedPlan(plan);
        applyPlan(plan, fromAi);
    }

    private void generateTrainingWithAi(final WorkoutPlan localPlan, final String intentText, final boolean unknown) {
        final int generation = ++planGeneration;
        final List<Exercise> safe = engine().safeCandidates(lastInput);
        if (safe.isEmpty()) {
            applyGeneratedPlan(localPlan, false);
            Toast.makeText(this, "已生成：" + localPlan.title()
                    + "（" + localPlan.items().size() + " 个动作）", Toast.LENGTH_SHORT).show();
            return;
        }
        aiThinking = true;
        renderAdHocSetup();
        String prompt = buildTrainingPrompt(localPlan, safe, intentText, unknown);
        geminiClient.generate(aiApiKey, aiModel, prompt, new GeminiClient.Callback() {
            @Override
            public void onResult(String text) {
                if (generation != planGeneration || inSession || isDestroyed()) return;
                WorkoutPlan aiPlan = parseTrainingAi(text, localPlan, safe);
                if (aiPlan != null) {
                    applyGeneratedPlan(aiPlan, true);
                    Toast.makeText(MainActivity.this, "AI 已生成：" + aiPlan.title()
                            + "（" + aiPlan.items().size() + " 个动作）", Toast.LENGTH_SHORT).show();
                } else {
                    applyGeneratedPlan(localPlan, false);
                    Toast.makeText(MainActivity.this, "AI 结果不可用，已用本地推荐", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onError(String message) {
                if (generation != planGeneration || inSession || isDestroyed()) return;
                applyGeneratedPlan(localPlan, false);
                Toast.makeText(MainActivity.this, "AI 暂时不可用（" + message + "），已用本地推荐",
                        Toast.LENGTH_LONG).show();
            }
        });
    }

    private String buildTrainingPrompt(WorkoutPlan localPlan, List<Exercise> safe,
            String intentText, boolean unknown) {
        int targetCount = Math.max(1, localPlan.items().size());
        StringBuilder builder = new StringBuilder();
        builder.append("你是健身教练助手。下面列出的候选动作已经按用户的伤痛、器械和证据做过安全过滤，")
                .append("你只能从这些候选里挑选和排序，绝对不要臆造列表之外的动作。\n");
        builder.append("用户目标：").append(unknown || intentText.trim().length() == 0
                ? "不确定，想练全身" : intentText.trim()).append("\n");
        builder.append("强度：").append(localPlan.intensity().label())
                .append("，建议动作数：约 ").append(targetCount).append(" 个。\n");
        List<String> recentIds = recentExerciseIdsForRecommendation();
        if (!recentIds.isEmpty()) {
            builder.append("以下动作刚完成或刚推荐过；同一动作模式有其他安全候选时优先轮换，不要为了变化改变训练结构：")
                    .append(join(recentIds)).append("。\n");
        }
        builder.append("下面的候选动作已在本地按用户身体状况过滤过，请把低风险、基础的动作排在前面。\n");
        builder.append("候选动作（id | 名称 | 部位 | 动作模式 | 难度）：\n");
        for (Exercise exercise : safe) {
            builder.append(exercise.id()).append(" | ").append(exercise.name())
                    .append(" | ").append(join(exercise.targetRegions()))
                    .append(" | ").append(join(exercise.movementPatterns()))
                    .append(" | ").append(exercise.difficulty()).append("\n");
        }
        if (targetCount == 1) {
            builder.append("这是超短或单动作训练，只选 1 个最贴合当前状态的动作。\n");
        } else {
            builder.append("请挑选并排序一套贴合用户目标的训练；如果是全身则尽量覆盖 推/拉/下肢/核心。\n");
        }
        builder.append("只返回 JSON：{\"ids\": [\"按顺序的动作id\"], \"reason\": \"一段中文，说明这套怎么贴合用户的目标和身体状况\"}。");
        builder.append("ids 必须全部来自上面的候选 id，数量控制在 ").append(targetCount).append(" 个左右。");
        return builder.toString();
    }

    private WorkoutPlan parseTrainingAi(String text, WorkoutPlan localPlan, List<Exercise> safe) {
        try {
            JSONObject object = new JSONObject(text);
            JSONArray ids = object.optJSONArray("ids");
            if (ids == null || ids.length() == 0) {
                return null;
            }
            Map<String, Exercise> byId = new HashMap<String, Exercise>();
            for (Exercise exercise : safe) {
                byId.put(exercise.id(), exercise);
            }
            Intensity intensity = localPlan.intensity();
            List<WorkoutItem> items = new ArrayList<WorkoutItem>();
            Set<String> used = new HashSet<String>();
            int maxItems = Math.max(1, localPlan.items().size());
            for (WorkoutItem original : localPlan.items()) {
                Exercise chosen = original.exercise();
                for (int i = 0; i < ids.length(); i++) {
                    Exercise e = byId.get(ids.optString(i));
                    if (e != null && !used.contains(e.id()) && TrainingSelection.sameRole(original.exercise(), e)
                            && TrainingSelection.preference(e, intensity) >= TrainingSelection.preference(original.exercise(), intensity)) {
                        chosen = e; break;
                    }
                }
                if (!used.add(chosen.id())) return null;
                Prescription dose = ExerciseTempo.effective(chosen, original.prescription());
                items.add(new WorkoutItem(chosen, dose, favoriteIds.contains(chosen.id()),
                        TrainingSelection.role(chosen) + " · 按当前目标安排", original.restAfterSeconds(), original.weight()));
            }
            if (items.isEmpty()) {
                return null;
            }
            if (planBudgetMinutes > 0 && timeModel().sessionSeconds(items) > planBudgetMinutes * 60) return null;
            String reason = object.optString("reason", "").trim();
            if (reason.length() == 0) {
                reason = localPlan.recommendationReason();
            }
            // AI 可能选出不同数量的动作，时长要按它选的重新算，不能沿用本地方案的分钟数。
            return new WorkoutPlan(localPlan.title(), intensity,
                    timeModel().sessionMinutes(items),
                    items, reason, localPlan.avoidanceNotes(), localPlan.safetyMessage(),
                    localPlan.isSafetyLimited());
        } catch (Exception ignored) {
            return null;
        }
    }

    private boolean aiConfigured() {
        return aiEnabled && aiApiKey != null && aiApiKey.trim().length() > 0;
    }

    /** Key used by web-search features (全网搜菜谱、链接解析); falls back to the main key when unset. */
    private String webSearchApiKey() {
        if (isGroqSearchProvider()) {
            return aiSearchApiKey == null ? "" : aiSearchApiKey.trim();
        }
        return aiSearchApiKey != null && aiSearchApiKey.trim().length() > 0 ? aiSearchApiKey : aiApiKey;
    }

    private String webSearchModel() {
        if (isGroqSearchProvider()) {
            return aiSearchModel == null || aiSearchModel.trim().length() == 0
                    ? GroqEndpoint.DEFAULT_MODEL : aiSearchModel.trim();
        }
        return aiSearchModel != null && aiSearchModel.trim().length() > 0
                ? GeminiModelName.normalize(aiSearchModel) : GeminiModelName.normalize(aiModel);
    }

    private boolean isGroqSearchProvider() {
        return SEARCH_PROVIDER_GROQ.equals(aiSearchProvider);
    }

    private boolean webSearchConfigured() {
        return aiEnabled && webSearchApiKey().length() > 0;
    }

    private void generateWithWebProvider(String prompt, final GeminiClient.Callback callback) {
        if (!isGroqSearchProvider()) {
            geminiClient.generateWithGoogleSearch(webSearchApiKey(), webSearchModel(), prompt, callback);
            return;
        }
        groqClient.generate(webSearchApiKey(), aiSearchEndpoint, webSearchModel(), prompt, false,
                new GroqClient.Callback() {
                    @Override
                    public void onResult(String text) {
                        callback.onResult(text);
                    }

                    @Override
                    public void onError(String message) {
                        callback.onError(message);
                    }
                });
    }

    private void generateUrlWithWebProvider(String prompt, final GeminiClient.Callback callback) {
        if (!isGroqSearchProvider()) {
            geminiClient.generateWithUrlContext(webSearchApiKey(), webSearchModel(), prompt, callback);
            return;
        }
        groqClient.generate(webSearchApiKey(), aiSearchEndpoint, webSearchModel(), prompt, true,
                new GroqClient.Callback() {
                    @Override
                    public void onResult(String text) {
                        callback.onResult(text);
                    }

                    @Override
                    public void onError(String message) {
                        callback.onError(message);
                    }
                });
    }

    private void persistWebSearchModelFallback(String requestedModel, String fallbackModel) {
        aiSearchModel = fallbackModel;
        saveState();
        Toast.makeText(this, "搜索模型 " + requestedModel + " 不可用，已切换为 " + fallbackModel,
                Toast.LENGTH_LONG).show();
    }

    private RecommendationInput.Builder inputBuilder(String text, boolean unknown) {
        RecommendationInput.Builder builder = new RecommendationInput.Builder()
                .intentText(text)
                .intensity(selectedIntensity)
                .targetMinutes(selectedDurationMinutes)
                .includeUserUnverified(false)
                .favoriteExercises(favoriteIds)
                .verifiedExercises(reviewedIdsForRecommendation());
        if (unknown) {
            builder.unknownWorkout();
        }
        for (String item : equipment) {
            builder.equipment(item);
        }
        addPain(builder, shoulderPain, "shoulder");
        addPain(builder, lowerBackPain, "lower_back");
        addPain(builder, kneePain, "knee");
        return builder;
    }

    private void addPain(RecommendationInput.Builder builder, PainSeverity severity, String key) {
        if (severity == null) {
            return;
        }
        if ("shoulder".equals(key)) {
            builder.pain(PainPoint.shoulder(severity));
        } else if ("lower_back".equals(key)) {
            builder.pain(PainPoint.lowerBack(severity));
        } else if ("knee".equals(key)) {
            builder.pain(PainPoint.knee(severity));
        }
    }

    private void renderPlan() {
        LinearLayout wrap = card();
        if (currentPlanFromAi) {
            TextView badge = text("AI 推荐", 11, Typeface.BOLD, GREEN);
            badge.setPadding(dp(8), dp(3), dp(8), dp(3));
            badge.setBackground(bg(GREEN_SOFT, dp(7), GREEN_SOFT, 0));
            LinearLayout.LayoutParams badgeLp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            badgeLp.setMargins(0, 0, 0, dp(6));
            wrap.addView(badge, badgeLp);
        }
        wrap.addView(text(currentPlan.title(), 22, Typeface.BOLD, INK));
        // 时长按每个动作的实际处方算出来（组数 × 次数 × 节奏 + 组间休息 + 切换），不是回显你选的分钟数。
        wrap.addView(text("预计主课 " + currentPlan.estimatedMinutes() + " 分钟 · 另建议热身 "
                + SessionTimeModel.WARMUP_ADVICE_MINUTES + " / 放松 "
                + SessionTimeModel.COOLDOWN_ADVICE_MINUTES + " 分钟", 14, Typeface.BOLD, BLUE));
        wrap.addView(text("科学来源：ACSM / HHS / ACE", 12, Typeface.NORMAL, MUTED));
        wrap.addView(space(10));
        wrap.addView(noteBox(currentPlan.safetyMessage(), currentPlan.isSafetyLimited() ? CORAL : GREEN));
        if (!currentPlan.avoidanceNotes().isEmpty()) {
            wrap.addView(space(8));
            for (String note : currentPlan.avoidanceNotes()) {
                wrap.addView(text("· " + note, 13, Typeface.NORMAL, MUTED));
            }
        }
        content.addView(wrap);

        for (int i = 0; i < activeItems.size(); i++) {
            content.addView(exercisePlanCard(i, activeItems.get(i)));
        }

        LinearLayout reason = card();
        reason.addView(section("为什么推荐"));
        reason.addView(text(currentPlan.recommendationReason(), 14, Typeface.NORMAL, MUTED));
        reason.addView(space(10));
        reason.addView(text("点“开始训练”进入引导模式：逐个动作、自动计时，完成或放弃后自动进入下一个。", 13, Typeface.NORMAL, MUTED));
        reason.addView(space(8));
        reason.addView(button("▶ 开始训练（自动计时）", GREEN, Color.WHITE, v -> startSession()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(50)));
        content.addView(reason);
    }

    private View exercisePlanCard(int index, WorkoutItem item) {
        LinearLayout card = card();
        card.addView(mediaStrip(item.exercise()));
        card.addView(space(10));
        LinearLayout head = new LinearLayout(this);
        head.setOrientation(LinearLayout.HORIZONTAL);
        TextView name = text((index + 1) + ". " + item.exercise().name(), 18, Typeface.BOLD, INK);
        head.addView(name, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        if (favoriteIds.contains(item.exercise().id())) {
            TextView heart = text("♥", 18, Typeface.BOLD, HEART_RED);
            heart.setGravity(Gravity.CENTER);
            head.addView(heart);
        }
        card.addView(head);
        card.addView(text(join(item.exercise().targetRegions()) + " · " + join(item.exercise().movementPatterns()), 13, Typeface.NORMAL, MUTED));
        card.addView(space(6));
        card.addView(text(item.prescription().compactLabel(), 15, Typeface.BOLD, BLUE));
        card.addView(text(item.reason(), 13, Typeface.NORMAL, MUTED));
        if (!item.exercise().substitutions().isEmpty()) {
            card.addView(text("替代：" + join(item.exercise().substitutions()), 13, Typeface.NORMAL, MUTED));
        }
        card.addView(space(10));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(button("替换", BLUE, Color.WHITE, v -> replaceItem(index)),
                new LinearLayout.LayoutParams(0, dp(42), 1f));
        row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        row.addView(button("详情", Color.rgb(236, 240, 234), INK, v -> showExerciseDetail(item.exercise())),
                new LinearLayout.LayoutParams(0, dp(42), 1f));
        card.addView(row);
        return card;
    }

    private void replaceItem(int index) {
        if (lastInput == null || index < 0 || index >= activeItems.size()) {
            return;
        }
        List<String> ids = new ArrayList<String>();
        for (WorkoutItem item : activeItems) {
            ids.add(item.exercise().id());
        }
        WorkoutItem replacement = engine().replacementFor(activeItems.get(index), lastInput, ids);
        if (replacement == null) {
            Toast.makeText(this, "暂时没有更安全且器械匹配的替代动作", Toast.LENGTH_SHORT).show();
            return;
        }
        WorkoutItem original = activeItems.get(index);
        Prescription suggested = replacement.prescription();
        Prescription matched = suggested.kind() == Prescription.Kind.HOLD
                ? Prescription.hold(original.prescription().sets(), suggested.holdSeconds(),
                        original.prescription().rpe(), original.prescription().restSeconds(), suggested.perSide())
                : new Prescription(original.prescription().sets(), suggested.reps(), original.prescription().rpe(),
                        original.prescription().restSeconds()).withPerSide(suggested.perSide())
                        .withSecondsPerRep(suggested.secondsPerRep());
        replacement = new WorkoutItem(replacement.exercise(),
                matched,
                favoriteIds.contains(replacement.exercise().id()), replacement.reason(), original.restAfterSeconds(), original.weight());
        List<WorkoutItem> proposed = new ArrayList<WorkoutItem>(activeItems);
        proposed.set(index, replacement);
        if (planBudgetMinutes > 0 && timeModel().sessionSeconds(proposed) > planBudgetMinutes * 60) {
            Toast.makeText(this, "这个替换会超出时间预算，已保留原动作。", Toast.LENGTH_SHORT).show();
            return;
        }
        activeItems.set(index, replacement);
        persistWorkoutDraft();
        renderWorkoutPreview();
    }

    private void startSession() {
        if (inSession) { renderSession(); return; }
        if (!checkReviewedSelection(activeItems)) return;
        if (!checkRequiredEquipmentSelection(activeItems)) return;
        if (activeItems.isEmpty()) {
            Toast.makeText(this, "请先生成一套训练组合", Toast.LENGTH_SHORT).show();
            return;
        }
        inSession = true;
        sessionIndex = 0;
        exerciseRunning = false;
        sessionPhase = SessionPhase.PREPARE;
        workoutClock.start(SystemClock.elapsedRealtime());
        sessionSetIndex = 0;
        inRest = false;
        exerciseStartedActiveMillis = 0;
        sessionStartEpochMillis = System.currentTimeMillis();
        sessionHadPause = false;
        sessionResults.clear();
        sessionStats.clear();
        voiceCues.begin();
        renderSession();
    }

    /** 引导式训练的四个阶段。 */
    private enum SessionPhase {
        /** 看示范、准备开始。 */
        PREPARE,
        /** 三二一倒数。 */
        COUNT_IN,
        /** 正在做：计时动作走倒计时，计次动作走秒表。 */
        WORK,
        /** 组间休息倒计时。 */
        REST
    }

    private void renderSession() {
        if (!inSession || activeItems.isEmpty()) { renderTraining(); return; }
        currentTab = "training";
        clear();
        sessionVisible = true;
        trainingPage = "session";
        WorkoutItem item = activeItems.get(sessionIndex);
        Exercise exercise = item.exercise();
        Prescription prescription = item.prescription();
        int totalSets = Math.max(1, prescription.sets());
        boolean paused = workoutClock.isPaused();
        long now = SystemClock.elapsedRealtime();

        content.addView(title(paused ? "休息一下，没关系" : "专心这一组",
                "动作 " + (sessionIndex + 1) + " / " + activeItems.size() + " · "
                + (voiceEnabled ? "语音已开启" : "语音已关闭")));
        content.addView(progressBar(sessionIndex / (float) activeItems.size()));
        content.addView(space(12));
        content.addView(text(exercise.name(), 26, Typeface.BOLD, INK));
        content.addView(text(workoutItemLabel(item), 14, Typeface.NORMAL, MUTED));
        content.addView(text(item.reason(), 14, Typeface.NORMAL, GREEN));

        LinearLayout ctrl = card();
        ctrl.setElevation(0);
        sessionChronometer = new Chronometer(this);
        sessionChronometer.setBase(now - workoutClock.elapsed(now));
        sessionChronometer.setFormat("本次已练 %s");
        sessionChronometer.setTextSize(13);
        sessionChronometer.setTextColor(MUTED);
        sessionChronometer.setGravity(Gravity.CENTER);
        if (!paused) sessionChronometer.start();
        ctrl.addView(sessionChronometer);
        ctrl.addView(space(8));
        TextView stage = text((sessionPhase == SessionPhase.REST ? (exerciseRunning ? "组间休息 · 接下来 " : "动作间休息 · 接下来 ") : "")
                + "第 " + (sessionSetIndex + 1) + " / " + totalSets + " 组", 15, Typeface.BOLD, GREEN);
        stage.setGravity(Gravity.CENTER);
        ctrl.addView(stage);
        if (paused) {
            TextView stopped = text(workoutClock.phaseDuration() > 0
                    ? (int) Math.ceil(workoutClock.remaining(now) / 1000.0) + " 秒"
                    : formatDuration(workoutClock.phaseElapsed(now) / 1000), 52, Typeface.BOLD, INK);
            stopped.setGravity(Gravity.CENTER);
            ctrl.addView(stopped);
            ctrl.addView(text("进度已保存。离开或锁屏会暂停，准备好再继续。", 13, Typeface.NORMAL, MUTED));
            ctrl.addView(space(12));
            ctrl.addView(button("继续训练 →", GREEN, Color.WHITE, v -> resumeWorkout()), fullButton());
        } else {
            switch (sessionPhase) {
                case PREPARE:
                    ctrl.addView(space(12));
                    ctrl.addView(text(prescription.kind() == Prescription.Kind.HOLD
                            ? "计时 " + prescription.holdSeconds() + " 秒" + (prescription.perSide() ? " / 侧" : "")
                            : "目标 " + prescription.reps() + " 次" + (prescription.perSide() && !prescription.reps().contains("侧") ? " / 侧" : ""),
                            26, Typeface.BOLD, INK));
                    ctrl.addView(text("先看下方示范，开始后倒数三秒。", 13, Typeface.NORMAL, MUTED));
                    ctrl.addView(space(12));
                    ctrl.addView(button("准备好了，开始这一组", GREEN, Color.WHITE, v -> startExercise()), fullButton());
                    break;
                case COUNT_IN:
                    ctrl.addView(countdownView(GREEN));
                    ctrl.addView(button("跳过倒数", GREEN_SOFT, GREEN, v -> beginWork()), fullButton());
                    break;
                case WORK:
                    if (prescription.kind() == Prescription.Kind.HOLD) {
                        ctrl.addView(countdownView(GREEN));
                    } else {
                        setChronometer = new Chronometer(this);
                        setChronometer.setBase(now - workoutClock.phaseElapsed(now));
                        setChronometer.setTextSize(58);
                        setChronometer.setTextColor(GREEN);
                        setChronometer.setGravity(Gravity.CENTER);
                        setChronometer.start();
                        ctrl.addView(setChronometer);
                    }
                    ctrl.addView(button(sessionSetIndex + 1 >= totalSets ? "完成动作 ✓" : "完成本组，休息", GREEN,
                            Color.WHITE, v -> completeSet()), fullButton());
                    break;
                case REST:
                    ctrl.addView(countdownView(BLUE));
                    LinearLayout row = new LinearLayout(this);
                    row.addView(button("+20 秒", GREEN_SOFT, GREEN, v -> {
                        workoutClock.extendPhase(20000);
                        lastSpokenSecond = -1;
                        persistWorkoutDraft();
                    }), new LinearLayout.LayoutParams(0, dp(52), 1));
                    row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
                    row.addView(button("休息好了", GREEN, Color.WHITE, v -> endRest()),
                            new LinearLayout.LayoutParams(0, dp(52), 2));
                    ctrl.addView(row);
                    break;
            }
            ctrl.addView(space(8));
            ctrl.addView(button("暂停一下", BG, INK, v -> { pauseWorkout(); renderSession(); }), fullButton());
        }
        content.addView(ctrl);
        content.addView(button("调整本动作安排", GREEN_SOFT, GREEN, v -> editActiveItem(sessionIndex)), fullButton());

        LinearLayout demonstration = card();
        demonstration.addView(text(reviewLabel(exercise), 13, Typeface.BOLD,
                isReviewed(exercise) ? GREEN : AMBER));
        demonstration.setElevation(0);
        View demo = mediaStrip(exercise);
        demo.setOnClickListener(v -> { pauseWorkout(); renderSession(); openMedia(exercise); });
        demonstration.addView(demo);
        if (!exercise.instructions().isEmpty()) {
            demonstration.addView(space(10));
            demonstration.addView(text(exercise.instructions().get(0), 14, Typeface.NORMAL, INK));
        }
        demonstration.addView(button("查看完整动作要点", BG, GREEN, v -> {
            pauseWorkout();
            renderSession();
            showExerciseDetail(exercise);
        }), fullButton());
        content.addView(demonstration);
        if (sessionIndex + 1 < activeItems.size()) content.addView(text("下一个 · "
                + activeItems.get(sessionIndex + 1).exercise().name(), 14, Typeface.NORMAL, MUTED));
        content.addView(button("跳过这个动作", BG, MUTED, v -> abandonExercise()), fullButton());
        if (!paused) getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        bottomNav.removeAllViews();
        bottomNav.addView(button("暂存，回到今天", GREEN_SOFT, GREEN, v -> {
            pauseWorkout(); renderTraining();
        }), new LinearLayout.LayoutParams(0, dp(52), 1));
        bottomNav.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        bottomNav.addView(button("结束并保存", SURFACE, MUTED, v -> confirmEndSession()),
                new LinearLayout.LayoutParams(0, dp(52), 1));
        persistWorkoutDraft();
        if (!paused) startTicker();
        scrollToTop();
    }

    private void pauseWorkout() {
        if (!inSession) return;
        sessionHadPause = true;
        workoutClock.pause(SystemClock.elapsedRealtime());
        stopTicker();
        if (sessionChronometer != null) sessionChronometer.stop();
        if (setChronometer != null) setChronometer.stop();
        voiceCues.end();
        persistWorkoutDraft();
    }

    private void resumeWorkout() {
        if (!checkReviewedSelection(activeItems.subList(sessionIndex, activeItems.size()))) return;
        workoutClock.resume(SystemClock.elapsedRealtime());
        voiceCues.begin();
        if (sessionPhase == SessionPhase.REST && workoutClock.remaining(SystemClock.elapsedRealtime()) <= 0) endRest();
        else renderSession();
    }

    private void startExercise() {
        exerciseRunning = true;
        inRest = false;
        sessionSetIndex = 0;
        startCountIn();
    }

    /** 三二一倒数：语音口令要有节拍，直接开始容易来不及摆姿势。 */
    private void startCountIn() {
        sessionPhase = SessionPhase.COUNT_IN;
        workoutClock.beginPhase(COUNT_IN_SECONDS * 1000L, SystemClock.elapsedRealtime());
        lastSpokenSecond = -1;
        switchSideSpoken = false;
        voiceCues.ready();
        renderSession();
    }

    /** 进入这一组：计时动作走倒计时，计次动作走秒表。 */
    private void beginWork() {
        Prescription prescription = activeItems.get(sessionIndex).prescription();
        sessionPhase = SessionPhase.WORK;
        if (sessionSetIndex == 0) exerciseStartedActiveMillis = workoutClock.elapsed(SystemClock.elapsedRealtime());
        lastSpokenSecond = -1;
        switchSideSpoken = false;
        if (prescription.kind() == Prescription.Kind.HOLD) {
            int seconds = Math.max(5, prescription.holdSeconds())
                    * (prescription.perSide() ? 2 : 1);
            workoutClock.beginPhase(seconds * 1000L, SystemClock.elapsedRealtime());
        } else {
            workoutClock.beginPhase(0, SystemClock.elapsedRealtime());
        }
        voiceCues.go();
        renderSession();
    }

    private void completeSet() {
        if (!inSession || workoutClock.isPaused() || sessionPhase != SessionPhase.WORK) return;
        int totalSets = Math.max(1, activeItems.get(sessionIndex).prescription().sets());
        if (sessionSetIndex + 1 >= totalSets) {
            completeExercise();
            return;
        }
        sessionSetIndex++;
        inRest = true;
        sessionPhase = SessionPhase.REST;
        int restSeconds = Math.max(0, activeItems.get(sessionIndex).prescription().restSeconds());
        if (restSeconds == 0) { startCountIn(); return; }
        workoutClock.beginPhase(restSeconds * 1000L, SystemClock.elapsedRealtime());
        lastSpokenSecond = -1;
        voiceCues.rest();
        renderSession();
    }

    private void endRest() {
        inRest = false;
        exerciseRunning = true;
        startCountIn();
    }

    // ------------------------------------------------------- 训练节拍器与语音口令

    /**
     * 每 200ms 校一次表。用 {@link SystemClock#elapsedRealtime()} 对齐而不是
     * {@code CountDownTimer} 的累加计时——后者会漂，报数就会踩不上秒。
     */
    private void startTicker() {
        stopTicker();
        sessionTicker.post(tickRunnable);
    }

    private void stopTicker() {
        sessionTicker.removeCallbacks(tickRunnable);
    }

    private void onTick() {
        if (!inSession || !sessionVisible || workoutClock.isPaused()) {
            return;
        }
        long now = SystemClock.elapsedRealtime();
        if (now - lastCheckpointRealtime >= 2000) persistWorkoutDraft();
        if (countdownLabel == null || workoutClock.phaseDuration() <= 0) {
            sessionTicker.postDelayed(tickRunnable, TICK_INTERVAL_MILLIS);
            return;
        }
        long remainingMillis = workoutClock.remaining(now);
        int remaining = (int) Math.ceil(Math.max(0, remainingMillis) / 1000.0);
        if (remaining != lastSpokenSecond) {
            countdownLabel.setText(String.valueOf(remaining));
            lastSpokenSecond = remaining;
            if (remaining >= 1 && remaining <= VOICE_COUNTDOWN_FROM) {
                voiceCues.count(remaining);
            }
        }
        // 单侧的等长动作在中点提醒换边。
        if (sessionPhase == SessionPhase.WORK && !switchSideSpoken && workoutClock.phaseDuration() > 0
                && activeItems.get(sessionIndex).prescription().perSide()
                && remainingMillis <= workoutClock.phaseDuration() / 2) {
            switchSideSpoken = true;
            voiceCues.switchSide();
        }

        if (remainingMillis <= 0) {
            stopTicker();
            advancePhase();
            return;
        }
        sessionTicker.postDelayed(tickRunnable, TICK_INTERVAL_MILLIS);
    }

    private void advancePhase() {
        switch (sessionPhase) {
            case COUNT_IN:
                beginWork();
                break;
            case WORK:
                // 计时动作到点自动结束这一组。
                voiceCues.done();
                completeSet();
                break;
            case REST:
                endRest();
                break;
            default:
                break;
        }
    }

    private TextView countdownView(int color) {
        countdownLabel = text(String.valueOf((int) Math.ceil(workoutClock.remaining(SystemClock.elapsedRealtime()) / 1000.0)),
                64, Typeface.BOLD, color);
        countdownLabel.setGravity(Gravity.CENTER);
        return countdownLabel;
    }

    private void recordExerciseResult(String status) {
        Exercise exercise = activeItems.get(sessionIndex).exercise();
        long seconds = exerciseRunning ? Math.max(0, workoutClock.elapsed(SystemClock.elapsedRealtime()) - exerciseStartedActiveMillis) / 1000 : 0;
        int totalSets = Math.max(1, activeItems.get(sessionIndex).prescription().sets());
        String mark = "完成".equals(status) ? "✓ " : sessionSetIndex > 0 ? "◐ " : "○ ";
        String setsInfo = "";
        if ("完成".equals(status)) {
            if (totalSets > 1) {
                setsInfo = " · " + totalSets + " 组";
            }
        } else if (sessionSetIndex > 0) {
            setsInfo = " · 已完成 " + sessionSetIndex + " 组";
        }
        String suffix = "完成".equals(status) ? "" : sessionSetIndex > 0 ? " · 提前结束" : " · 跳过";
        sessionResults.add(mark + exercise.name() + " · " + formatDuration(seconds) + setsInfo + suffix
                + (activeItems.get(sessionIndex).reason().isEmpty() ? "" : " · " + activeItems.get(sessionIndex).reason()));
        // 结构化地记下做了几组：周容量台账和恢复状态都要按动作 id 和组数聚合。
        int completedSets = "完成".equals(status) ? totalSets : sessionSetIndex;
        sessionStats.add(exercise.id() + "|" + completedSets + "|" + ("完成".equals(status) ? 1 : 0));
        exerciseRunning = false;
        inRest = false;
        sessionSetIndex = 0;
    }

    private void completeExercise() {
        int restAfter = activeItems.get(sessionIndex).restAfterSeconds();
        recordExerciseResult("完成");
        if (restAfter > 0 && sessionIndex + 1 < activeItems.size()) {
            sessionIndex++;
            sessionPhase = SessionPhase.REST;
            workoutClock.beginPhase(restAfter * 1000L, SystemClock.elapsedRealtime());
            lastSpokenSecond = -1; switchSideSpoken = false;
            voiceCues.rest(); renderSession();
        } else advanceOrFinish();
    }

    private void abandonExercise() {
        pauseWorkout();
        renderSession();
        new AlertDialog.Builder(this)
                .setTitle("放弃这个动作？")
                .setMessage("接下来要继续下一个动作，还是结束本次训练？")
                .setNeutralButton("取消", null)
                .setNegativeButton("结束训练", (dialog, which) -> {
                    recordExerciseResult("放弃");
                    finishSession();
                })
                .setPositiveButton("继续下一个", (dialog, which) -> {
                    recordExerciseResult("放弃");
                    workoutClock.resume(SystemClock.elapsedRealtime());
                    voiceCues.begin();
                    advanceOrFinish();
                })
                .show();
    }

    private void advanceOrFinish() {
        if (sessionIndex + 1 < activeItems.size()) {
            sessionIndex++;
            exerciseRunning = false;
            // 回到准备阶段：下一个动作要先看示范、再倒数进入，秒表也得从零开始。
            sessionPhase = SessionPhase.PREPARE;
            workoutClock.beginPhase(0, SystemClock.elapsedRealtime());
            lastSpokenSecond = -1;
            switchSideSpoken = false;
            stopTicker();
            voiceCues.next();
            renderSession();
        } else {
            finishSession();
        }
    }

    private void confirmEndSession() {
        pauseWorkout();
        renderSession();
        new AlertDialog.Builder(this)
                .setTitle("结束本次训练？")
                .setMessage("已练的动作会保存到记录，未做的标记为未做。")
                .setNegativeButton("取消", null)
                .setPositiveButton("结束并保存", (dialog, which) -> {
                    if (exerciseRunning) {
                        recordExerciseResult("放弃");
                    }
                    finishSession();
                })
                .show();
    }

    private void finishSession() {
        if (!inSession) return;
        long totalSeconds = workoutClock.elapsed(SystemClock.elapsedRealtime()) / 1000;
        List<String> lines = new ArrayList<String>(sessionResults);
        int doneCount = 0;
        for (String line : sessionResults) {
            if (line.startsWith("✓")) {
                doneCount++;
            }
        }
        for (int i = lines.size(); i < activeItems.size(); i++) {
            lines.add("○ " + activeItems.get(i).exercise().name() + " · 未做");
        }
        String time = new SimpleDateFormat("MM-dd HH:mm", Locale.CHINA).format(new Date());
        String planTitle = currentPlan != null ? currentPlan.title() : "训练";
        int predictedSeconds = timeModel().sessionSeconds(activeItems);
        SessionRecord saved = new SessionRecord(time, planTitle, activeItems.size(), doneCount,
                "", "", "",
                lines, formatDuration(totalSeconds), System.currentTimeMillis(),
                sessionStartEpochMillis, 0, 0, 0, "", 0, 0, false, "",
                new ArrayList<String>(sessionStats));
        saved.timingNote = sessionHadPause ? "训练用时已扣除暂停；手表数据按整段起止时间统计，可能包含暂停期间。" : "";
        for (int i = 0; i < activeItems.size(); i++) {
            WorkoutItem item = activeItems.get(i);
            int completed = 0; boolean finished = false;
            if (i < sessionStats.size()) {
                String[] stat = sessionStats.get(i).split("\\|");
                if (stat.length >= 3) { completed = Integer.parseInt(stat[1]); finished = "1".equals(stat[2]); }
            }
            saved.details.add(new WorkoutEntry(item.exercise().id(), item.exercise().name(), item.prescription(),
                    completed, finished, item.restAfterSeconds(), item.weight(), lines.get(i)));
        }
        trainingRecords.add(0, saved);
        // 全部动作都做完了才用来校准节奏系数；中途放弃的会把系数带偏。
        if (doneCount > 0 && doneCount == activeItems.size() && predictedSeconds > 0) {
            paceFactor = SessionTimeModel.calibrated(paceFactor, predictedSeconds, (int) totalSeconds);
        }
        if (pendingProgramKey.length() > 0 && doneCount == activeItems.size()) {
            markScheduledSessionDone(pendingProgramKey);
        }
        pendingProgramKey = "";
        if (healthPermissionGranted()) {
            syncHeartRateForRecord(recordKey(saved), true);
        }

        inSession = false;
        exerciseRunning = false;
        sessionPhase = SessionPhase.PREPARE;
        stopTicker();
        voiceCues.end();
        currentPlan = null;
        activeItems.clear();
        lastInput = null;
        sessionResults.clear();
        sessionStats.clear();
        saveState();
        Toast.makeText(this, "已保存本次训练（用时 " + formatDuration(totalSeconds) + "）", Toast.LENGTH_LONG).show();
        renderSessionCelebration(saved);
    }

    private String formatDuration(long seconds) {
        long m = seconds / 60;
        long s = seconds % 60;
        return m + ":" + (s < 10 ? "0" + s : String.valueOf(s));
    }

    private void renderSessionCelebration(SessionRecord record) {
        currentTab = "training";
        clear();
        trainingPage = "summary";
        content.addView(title("这一练，已收好", "训练记录已保存在本机"));
        int sets = recordedSets(record);
        LinearLayout reward = card();
        reward.setPadding(dp(24), dp(30), dp(24), dp(26));
        reward.setBackground(bg(Color.rgb(27, 66, 55), dp(24), GREEN, 0));
        TextView mark = text(sets > 0 ? "✓" : "·", 64, Typeface.BOLD, Color.rgb(218, 241, 177));
        mark.setGravity(Gravity.CENTER);
        reward.addView(mark);
        TextView headline = text(sets > 0 ? "今天这一步，算数。" : "今天先到这里。", 26, Typeface.BOLD, Color.WHITE);
        headline.setGravity(Gravity.CENTER);
        reward.addView(headline);
        reward.addView(space(10));
        TextView note = text(sets > 0 ? "不用每次都练满。做过的每一组，都留下了。" : "准备过也没关系，下次从这里开始。",
                14, Typeface.NORMAL, Color.rgb(200, 224, 210));
        note.setGravity(Gravity.CENTER);
        reward.addView(note);
        reward.addView(space(24));
        TextView numbers = text(record.duration + "   ·   " + sets + " 组", 32, Typeface.BOLD, Color.WHITE);
        numbers.setGravity(Gravity.CENTER);
        reward.addView(numbers);
        TextView label = text("训练用时（不含暂停）    /    实际完成", 12, Typeface.NORMAL, Color.rgb(200, 224, 210));
        label.setGravity(Gravity.CENTER);
        reward.addView(label);
        reward.addView(space(20));
        for (String line : record.itemLines) reward.addView(text(line, 13, Typeface.NORMAL, Color.WHITE));
        content.addView(reward);
        content.addView(weekFootprintCard());
        content.addView(button("记一下今天的感受", GREEN_SOFT, GREEN, v -> showSessionFeedback(recordKey(record))), fullButton());
        content.addView(space(10));
        content.addView(button("回到今天", GREEN, Color.WHITE, v -> renderTraining()), fullButton());
        renderBottomNav();
        scrollToTop();
        if (android.provider.Settings.Global.getFloat(getContentResolver(),
                android.provider.Settings.Global.ANIMATOR_DURATION_SCALE, 1f) > 0f) {
            reward.setAlpha(0f);
            reward.setTranslationY(dp(12));
            reward.animate().alpha(1f).translationY(0f).setDuration(350).start();
        }
    }

    private RadioGroup radioRow(String[] labels, int defaultIndex, int baseId) {
        RadioGroup group = new RadioGroup(this);
        group.setOrientation(RadioGroup.HORIZONTAL);
        for (int i = 0; i < labels.length; i++) {
            RadioButton button = new RadioButton(this);
            button.setText(labels[i]);
            button.setTextColor(INK);
            button.setId(baseId + i);
            if (i == defaultIndex) {
                button.setChecked(true);
            }
            group.addView(button);
        }
        return group;
    }

    private String selectedLabel(RadioGroup group, String[] labels, int baseId) {
        int index = group.getCheckedRadioButtonId() - baseId;
        return index >= 0 && index < labels.length ? labels[index] : "";
    }

    private View wrapScroll(View view) {
        HorizontalScrollView scroll = new HorizontalScrollView(this);
        scroll.setHorizontalScrollBarEnabled(false);
        scroll.addView(view);
        return scroll;
    }

    // Saved routines live in a separate preferences key; editing never overwrites workout progress.
    private String routineId = "";
    private String routineName = "", routineNote = "";
    private String routineRounds = "3", routineRoundRest = "60";
    private boolean routineCircuit;
    private final List<WorkoutItem> routineItems = new ArrayList<>();
    private EditText routineNameField, routineNoteField, routineRoundsField, routineRoundRestField;

    private JSONArray savedRoutines() throws org.json.JSONException {
        return new JSONArray(getSharedPreferences("fitness_state", MODE_PRIVATE).getString("routinesV1", "[]"));
    }

    private void routineError(Exception error) {
        new AlertDialog.Builder(this).setTitle("动作组未能完成")
                .setMessage(error.getMessage() == null ? "请检查动作组内容后重试" : error.getMessage())
                .setPositiveButton("知道了", null).show();
    }

    private void renderRoutines() {
        currentTab = "training";
        clear(); trainingPage = "routines";
        content.addView(title("我的动作组", "收藏自己的训练组合，按原顺序直接练"));
        content.addView(button("‹ 回到今天", BG, GREEN, v -> renderTraining()), fullButton());
        content.addView(space(8));
        content.addView(button("＋ 新建动作组", GREEN, Color.WHITE, v -> editRoutine(null)), fullButton());
        content.addView(space(8));
        content.addView(text("支持顺序训练与多轮循环。每个动作可设置计次或计时、组数、休息和重量备注。", 14, Typeface.NORMAL, MUTED));
        try {
            JSONArray saved = savedRoutines();
            if (saved.length() == 0) {
                content.addView(text("还没有保存的动作组。可以从动作库选动作，也可以新增库里没有的动作。", 16, Typeface.NORMAL, INK));
            }
            for (int i = 0; i < saved.length(); i++) {
                JSONObject data = saved.getJSONObject(i);
                LinearLayout row = card();
                row.addView(section(data.optString("name")));
                try {
                    WorkoutRoutine routine = RoutineCodec.decode(data, this::exerciseById);
                    row.addView(text((routine.circuit() ? "循环 " + routine.rounds() + " 轮" : "依次完成每个动作的所有组")
                            + " · 约 " + timeModel().sessionMinutes(routine.expand()) + " 分钟", 14, Typeface.NORMAL, GREEN));
                    row.addView(text(routine.note(), 13, Typeface.NORMAL, MUTED));
                    row.addView(space(8));
                    row.addView(button("练这组 →", GREEN, Color.WHITE, v -> launchRoutine(routine)), fullButton());
                    row.addView(space(8));
                    row.addView(button("编辑动作组", GREEN_SOFT, GREEN, v -> editRoutine(routine)), fullButton());
                } catch (Exception error) {
                    row.addView(text(error.getMessage(), 13, Typeface.NORMAL, CORAL));
                }
                row.addView(space(8));
                row.addView(button("删除动作组", BG, MUTED, v -> new AlertDialog.Builder(this)
                        .setTitle("删除「" + data.optString("name") + "」？")
                        .setMessage("只删除保存的组合，已完成的训练记录保留。")
                        .setNegativeButton("取消", null)
                        .setPositiveButton("删除", (d, w) -> removeRoutine(data.optString("id"))).show()), fullButton());
                content.addView(row);
            }
        } catch (Exception error) { routineError(error); }
        renderBottomNav(); scrollToTop();
    }

    private void removeRoutine(String id) {
        try {
            JSONArray saved = savedRoutines(), result = new JSONArray();
            for (int i = 0; i < saved.length(); i++) {
                if (!saved.getJSONObject(i).optString("id").equals(id)) result.put(saved.getJSONObject(i));
            }
            if (!getSharedPreferences("fitness_state", MODE_PRIVATE).edit().putString("routinesV1", result.toString()).commit())
                throw new IllegalStateException("保存失败，请重试");
            renderRoutines();
        } catch (Exception error) { routineError(error); }
    }

    private void editRoutine(WorkoutRoutine routine) {
        routineId = routine == null ? java.util.UUID.randomUUID().toString() : routine.id();
        routineName = routine == null ? "" : routine.name();
        routineNote = routine == null ? "" : routine.note();
        routineRounds = String.valueOf(routine == null ? 3 : routine.rounds());
        routineRoundRest = String.valueOf(routine == null ? 60 : routine.roundRest());
        routineCircuit = routine != null && routine.circuit();
        routineItems.clear();
        if (routine != null) routineItems.addAll(routine.items());
        renderRoutineEditor();
    }

    private void captureRoutineFields() {
        routineName = routineNameField.getText().toString();
        routineNote = routineNoteField.getText().toString();
        routineRounds = routineRoundsField.getText().toString();
        routineRoundRest = routineRoundRestField.getText().toString();
    }

    private EditText routineField(LinearLayout parent, String label, String value, boolean numeric) {
        parent.addView(text(label, 13, Typeface.BOLD, INK));
        EditText input = field(label, value, false, 50);
        input.setContentDescription(label);
        if (numeric) input.setInputType(InputType.TYPE_CLASS_NUMBER);
        parent.addView(input);
        return input;
    }

    private void renderRoutineEditor() {
        currentTab = "training";
        clear(); trainingPage = "routine_editor";
        content.addView(title("编排动作组", "按你想练的顺序保存"));
        content.addView(button("取消编辑", BG, MUTED, v -> leaveRoutineEditor()), fullButton());
        content.addView(space(10));
        LinearLayout header = card();
        routineNameField = routineField(header, "动作组名称", routineName, false);
        routineNoteField = routineField(header, "来源或训练备注（选填）", routineNote, false);
        routineRoundsField = routineField(header, "循环轮数（顺序训练时不使用）", routineRounds, true);
        routineRoundRestField = routineField(header, "轮间休息秒数", routineRoundRest, true);
        CheckBox circuit = new CheckBox(this);
        circuit.setText("循环训练：依次做完全部动作，再重复下一轮");
        circuit.setChecked(routineCircuit);
        circuit.setOnCheckedChangeListener((b, checked) -> routineCircuit = checked);
        header.addView(circuit);
        header.addView(text("不勾选时依次完成 A 的所有组，再做 B。循环时「组数」表示每轮做几组，通常填 1。", 13, Typeface.NORMAL, MUTED));
        content.addView(header);
        content.addView(button("保存动作组", GREEN, Color.WHITE, v -> saveRoutine()), fullButton());
        content.addView(space(8));
        content.addView(button("＋ 从动作库添加", GREEN_SOFT, GREEN, v -> { captureRoutineFields(); chooseRoutineExercise(); }), fullButton());
        content.addView(space(8));
        content.addView(button("＋ 新增库里没有的动作", BG, GREEN, v -> { captureRoutineFields(); newRoutineExercise(); }), fullButton());
        for (int i = 0; i < routineItems.size(); i++) {
            final int at = i;
            WorkoutItem item = routineItems.get(i);
            LinearLayout row = card();
            row.addView(section((i + 1) + "  " + item.exercise().name()));
            row.addView(text(reviewLabel(item.exercise()), 12, Typeface.BOLD, isReviewed(item.exercise()) ? GREEN : AMBER));
            row.addView(text(workoutItemLabel(item), 13, Typeface.NORMAL, MUTED));
            row.addView(text(item.reason(), 13, Typeface.NORMAL, GREEN));
            row.addView(space(8));
            row.addView(button("编辑次数、计时与重量", GREEN_SOFT, GREEN, v -> { captureRoutineFields(); editRoutineItem(item.exercise(), at); }), fullButton());
            row.addView(button("编辑动作备注", BG, MUTED, v -> {
                captureRoutineFields(); EditText note = new EditText(this); note.setText(item.reason());
                new AlertDialog.Builder(this).setTitle("动作备注").setView(note).setNegativeButton("取消", null)
                        .setPositiveButton("保存", (d, w) -> {
                            routineItems.set(at, new WorkoutItem(item.exercise(), item.prescription(), item.favorite(),
                                    note.getText().toString().trim(), item.restAfterSeconds(), item.weight())); renderRoutineEditor();
                        }).show();
            }), fullButton());
            row.addView(space(8));
            LinearLayout order = new LinearLayout(this);
            if (i > 0) {
                order.addView(button("上移", BG, GREEN, v -> { captureRoutineFields(); Collections.swap(routineItems, at, at - 1); renderRoutineEditor(); }), new LinearLayout.LayoutParams(0, dp(48), 1));
                order.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
            }
            if (i < routineItems.size() - 1) {
                order.addView(button("下移", BG, GREEN, v -> { captureRoutineFields(); Collections.swap(routineItems, at, at + 1); renderRoutineEditor(); }), new LinearLayout.LayoutParams(0, dp(48), 1));
                order.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
            }
            order.addView(button("移除", BG, MUTED, v -> { captureRoutineFields(); routineItems.remove(at); renderRoutineEditor(); }), new LinearLayout.LayoutParams(0, dp(48), 1));
            row.addView(order); content.addView(row);
        }
        // Navigation is explicit while editing, to prevent an accidental tab tap from discarding work.
        bottomNav.removeAllViews();
        bottomNav.addView(button("保存动作组", GREEN, Color.WHITE, v -> saveRoutine()), new LinearLayout.LayoutParams(-1, dp(52)));
        scrollToTop();
    }

    private void leaveRoutineEditor() {
        new AlertDialog.Builder(this).setTitle("离开动作组编辑？").setMessage("未保存的修改将丢失。")
                .setNegativeButton("继续编辑", null).setPositiveButton("放弃修改", (d, w) -> renderRoutines()).show();
    }

    private void saveRoutine() {
        captureRoutineFields();
        try {
            WorkoutRoutine routine = new WorkoutRoutine(routineId, routineName, routineNote, routineCircuit,
                    routineCircuit ? Integer.parseInt(routineRounds) : 1,
                    routineCircuit ? Integer.parseInt(routineRoundRest) : 0, routineItems);
            JSONArray saved = savedRoutines(), result = new JSONArray();
            boolean replaced = false;
            for (int i = 0; i < saved.length(); i++) {
                JSONObject old = saved.getJSONObject(i);
                if (old.optString("id").equals(routineId)) { result.put(RoutineCodec.encode(routine)); replaced = true; }
                else result.put(old);
            }
            if (!replaced) result.put(RoutineCodec.encode(routine));
            if (!getSharedPreferences("fitness_state", MODE_PRIVATE).edit().putString("routinesV1", result.toString()).commit())
                throw new IllegalStateException("保存失败，请重试");
            Toast.makeText(this, "动作组已保存", Toast.LENGTH_SHORT).show();
            renderRoutines();
        } catch (NumberFormatException error) { routineError(new IllegalArgumentException("轮数和休息请填写整数")); }
        catch (Exception error) { routineError(error); }
    }

    private void chooseRoutineExercise() {
        LinearLayout box = new LinearLayout(this); box.setOrientation(LinearLayout.VERTICAL); box.setPadding(dp(16), 0, dp(16), 0);
        EditText search = routineField(box, "搜索名称或器械", "", false);
        box.addView(text(reviewedOnly ? "仅显示已复核动作" : "全部动作 · 标签显示复核状态", 13, Typeface.BOLD, GREEN));
        android.widget.ListView list = new android.widget.ListView(this);
        box.addView(list, new LinearLayout.LayoutParams(-1, dp(340)));
        List<Exercise> matches = new ArrayList<>();
        android.widget.ArrayAdapter<String> adapter = new android.widget.ArrayAdapter<>(this, android.R.layout.simple_list_item_1, new ArrayList<String>());
        list.setAdapter(adapter);
        Runnable update = () -> {
            matches.clear(); adapter.clear();
            String query = search.getText().toString().toLowerCase(Locale.ROOT).trim();
            for (Exercise e : trainingExercises()) {
                if ((e.name() + " " + equipmentLabel(e)).toLowerCase(Locale.ROOT).contains(query)) {
                    matches.add(e); adapter.add(e.name() + " · " + reviewLabel(e) + " · " + equipmentLabel(e));
                    if (matches.size() >= 100) break;
                }
            }
            adapter.notifyDataSetChanged();
        };
        search.addTextChangedListener(new android.text.TextWatcher() {
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            public void onTextChanged(CharSequence s, int start, int before, int count) { update.run(); }
            public void afterTextChanged(android.text.Editable s) {}
        });
        AlertDialog dialog = new AlertDialog.Builder(this).setTitle("选择动作（最多显示 100 项）").setView(box).setNegativeButton("取消", null).create();
        list.setOnItemClickListener((parent, view, position, id) -> { Exercise e = matches.get(position); dialog.dismiss(); editRoutineItem(e, -1); });
        update.run(); dialog.show();
    }

    private void newRoutineExercise() {
        LinearLayout box = new LinearLayout(this); box.setOrientation(LinearLayout.VERTICAL); box.setPadding(dp(16), 0, dp(16), 0);
        EditText name = routineField(box, "动作名称", "", false);
        EditText instructions = routineField(box, "动作要点或来源", "", false);
        EditText region = routineField(box, "主要部位（如腿、背、有氧）", "其他", false);
        box.addView(text("器械", 13, Typeface.BOLD, INK));
        final Spinner equipmentPicker = customEquipmentPicker(new ArrayList<String>(Arrays.asList("自重")));
        box.addView(equipmentPicker, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));
        AlertDialog dialog = new AlertDialog.Builder(this).setTitle("新增个人动作").setView(box)
                .setNegativeButton("取消", null).setPositiveButton("添加并设处方", null).create();
        dialog.setOnShowListener(d -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            if (name.getText().toString().trim().isEmpty()) { name.setError("请填写名称"); return; }
            Exercise e = customExercise("custom_routine_" + java.util.UUID.randomUUID(), name.getText().toString().trim(),
                    Arrays.asList(region.getText().toString().trim()), instructions.getText().toString(), "",
                    Arrays.asList(String.valueOf(equipmentPicker.getSelectedItem())));
            customExercises.add(e); saveState(); dialog.dismiss(); editRoutineItem(e, -1);
        })); dialog.show();
    }

    private void editRoutineItem(Exercise e, int index) {
        WorkoutItem old = index < 0 ? new WorkoutItem(e, ExerciseTempo.effective(e,
                e.prescription(Intensity.MEDIUM)).withSets(1).withRestSeconds(30), false, "", 75) : routineItems.get(index);
        WorkoutDoseEditor.show(this, e.name(), old.prescription(), old.restAfterSeconds(), old.weight(), -1, 1,
                (dose, after, weight, done) -> {
                    WorkoutItem item = new WorkoutItem(e, dose, favoriteIds.contains(e.id()), old.reason(), after, weight);
                    if (index < 0) { if (routineItems.size() >= 30) throw new IllegalArgumentException("最多保存 30 个动作"); routineItems.add(item); }
                    else routineItems.set(index, item);
                    renderRoutineEditor();
                });
    }

    private void editActiveItem(int index) {
        if (index < 0 || index >= activeItems.size()) return;
        if (inSession) { pauseWorkout(); renderSession(); }
        WorkoutItem old = activeItems.get(index);
        int minimum = inSession && index == sessionIndex ? sessionSetIndex + 1 : 1;
        WorkoutDoseEditor.show(this, old.exercise().name(), old.prescription(), old.restAfterSeconds(), old.weight(), -1, minimum,
                (dose, after, weight, done) -> {
                    activeItems.set(index, new WorkoutItem(old.exercise(), dose, old.favorite(), old.reason(), after, weight));
                    if (inSession && index == sessionIndex) {
                        long now = SystemClock.elapsedRealtime();
                        if (sessionPhase == SessionPhase.REST && exerciseRunning)
                            workoutClock.setPhaseDuration(dose.restSeconds() * 1000L);
                        if (sessionPhase == SessionPhase.WORK) {
                            long target = dose.kind() == Prescription.Kind.HOLD ? dose.holdSeconds() * (dose.perSide() ? 2L : 1L) * 1000L : 0;
                            workoutClock.setPhaseDuration(target);
                            switchSideSpoken = false;
                        }
                    }
                    currentPlan = new WorkoutPlan(currentPlan.title(), currentPlan.intensity(), timeModel().sessionMinutes(activeItems),
                            activeItems, currentPlan.recommendationReason(), currentPlan.avoidanceNotes(), currentPlan.safetyMessage(), currentPlan.isSafetyLimited());
                    persistWorkoutDraft();
                    if (inSession) renderSession(); else renderWorkoutPreview();
                });
    }

    private void launchRoutine(WorkoutRoutine routine) {
        if (inSession) { renderSession(); return; }
        if (!checkReviewedSelection(routine.items())) return;
        List<String> conflicts = new ArrayList<>();
        Set<String> allowedIds = new HashSet<>();
        for (Exercise e : engine().safeCandidates(inputBuilder("", true).includeUserUnverified(true).build())) allowedIds.add(e.id());
        for (WorkoutItem item : routine.items()) {
            Exercise e = item.exercise();
            if (!e.hasAvailableEquipment(new ArrayList<>(equipment))) conflicts.add(e.name() + "：设置中未启用 " + equipmentLabel(e));
            else if (!allowedIds.contains(e.id())) conflicts.add(e.name() + "：与当前伤痛或动作状态冲突，请先编辑替换动作");
        }
        if (!conflicts.isEmpty()) {
            new AlertDialog.Builder(this).setTitle("先检查动作组").setMessage(join(conflicts))
                    .setNegativeButton("返回", null).setPositiveButton("编辑动作组", (d,w) -> editRoutine(routine)).show(); return;
        }
        planGeneration++; pendingProgramKey = ""; lastInput = null; planBudgetMinutes = 0;
        currentTab = "training";
        List<WorkoutItem> items = routine.expand();
        applyPlan(new WorkoutPlan(routine.name(), Intensity.MEDIUM, timeModel().sessionMinutes(items), items,
                (routine.circuit() ? "按保存顺序循环 " + routine.rounds() + " 轮，轮间休息 " + routine.roundRest() + " 秒。" : "依次完成各动作全部组数。") + routine.note(),
                Collections.emptyList(), "个人编排 · 重量与训练量按你的保存值执行，可在动作组中调整。", false), false);
    }

    private void renderLibrary(String filter) {
        currentTab = "library";
        if (deletedCategories.contains(filter)) {
            filter = "全部";
        }
        if (!filter.equals(libraryFilter)) {
            libraryVisibleLimit = 60;
        }
        libraryFilter = filter;
        clear();
        content.addView(title("动作库", "共 " + (seedExercises.size() + datasetExercises.size())
                + " 个默认动作·按部位分类"));
        List<Exercise> inventory = allExercises();
        int reviewedCount = 0;
        for (Exercise e : inventory) if (isReviewed(e)) reviewedCount++;
        content.addView(text("已复核 " + reviewedCount + " · 未复核 " + (inventory.size() - reviewedCount)
                + " · 动态示范", 12, Typeface.BOLD, GREEN));
        content.addView(button("复核筛选：" + libraryReviewFilter, GREEN_SOFT, GREEN, v -> {
            String[] filters = {"全部状态", "已复核", "未复核", "待补图", "待修图", "待核逻辑"};
            new AlertDialog.Builder(this).setTitle("筛选复核状态（可叠加部位和搜索）")
                    .setItems(filters, (d, which) -> {
                        libraryReviewFilter = filters[which]; libraryVisibleLimit = 60;
                        renderLibrary(libraryFilter);
                    }).show();
        }), fullButton());
        if (!exerciseReviews.loadError.isEmpty()) content.addView(text(exerciseReviews.loadError, 12, Typeface.NORMAL, CORAL));
        content.addView(space(8));

        content.addView(button("我的动作组", GREEN_SOFT, GREEN, v -> renderRoutines()), fullButton());
        LinearLayout tools = new LinearLayout(this);
        tools.setOrientation(LinearLayout.HORIZONTAL);
        tools.addView(button("新增动作", GREEN, Color.WHITE, v -> showCustomForm(null)),
                new LinearLayout.LayoutParams(0, dp(44), 1f));
        tools.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        tools.addView(button("待确认 " + pendingShares.size(), CORAL, Color.WHITE, v -> renderLibrary("待确认")),
                new LinearLayout.LayoutParams(0, dp(44), 1f));
        content.addView(tools);
        content.addView(space(8));

        LinearLayout searchRow = new LinearLayout(this);
        searchRow.setOrientation(LinearLayout.HORIZONTAL);
        final EditText search = new EditText(this);
        search.setHint("搜索动作、肌群或器械");
        search.setSingleLine(true);
        search.setText(libraryQuery);
        search.setSelection(search.getText().length());
        search.setImeOptions(EditorInfo.IME_ACTION_SEARCH);
        searchRow.addView(search, new LinearLayout.LayoutParams(0, dp(46), 1f));
        searchRow.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
        searchRow.addView(button("搜索", BLUE, Color.WHITE,
                v -> applyLibrarySearch(search.getText().toString())),
                new LinearLayout.LayoutParams(dp(70), dp(46)));
        search.setOnEditorActionListener((view, actionId, event) -> {
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                applyLibrarySearch(search.getText().toString());
                return true;
            }
            return false;
        });
        content.addView(searchRow);
        if (libraryQuery.length() > 0) {
            TextView clearSearch = text("当前搜索：" + libraryQuery + "  × 清除", 12, Typeface.BOLD, BLUE);
            clearSearch.setPadding(dp(4), dp(5), dp(4), dp(7));
            clearSearch.setOnClickListener(v -> applyLibrarySearch(""));
            content.addView(clearSearch);
        } else {
            content.addView(space(8));
        }

        LinearLayout pane = new LinearLayout(this);
        pane.setOrientation(LinearLayout.HORIZONTAL);
        // Fill the remaining viewport (ScrollView uses fillViewport), so the sidebar
        // and grid get the full height and never get cut off by the bottom nav.
        LinearLayout.LayoutParams paneParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f);
        paneParams.setMargins(0, 0, 0, 0);
        pane.setLayoutParams(paneParams);
        pane.setMinimumHeight(dp(360));

        ScrollView sideScroll = new ScrollView(this);
        sideScroll.setVerticalScrollBarEnabled(false);
        LinearLayout side = new LinearLayout(this);
        side.setOrientation(LinearLayout.VERTICAL);
        for (String category : libraryCategories()) {
            side.addView(sidebarItem(category));
        }
        sideScroll.addView(side);
        pane.addView(sideScroll, new LinearLayout.LayoutParams(dp(82), ViewGroup.LayoutParams.MATCH_PARENT));
        pane.addView(space(8), new LinearLayout.LayoutParams(dp(8), ViewGroup.LayoutParams.MATCH_PARENT));

        ScrollView rightScroll = new ScrollView(this);
        rightScroll.setClipToPadding(false);
        rightScroll.setClipChildren(false);
        LinearLayout right = new LinearLayout(this);
        right.setOrientation(LinearLayout.VERTICAL);
        right.setClipChildren(false);
        right.setClipToPadding(false);
        right.setPadding(dp(2), 0, dp(2), dp(8));
        if ("待确认".equals(libraryFilter)) {
            addPendingShares(right);
        } else {
            if (canDeleteCategory(libraryFilter)) {
                right.addView(button("删除当前分类", Color.rgb(248, 235, 232), CORAL,
                        v -> confirmDeleteCategory(libraryFilter)),
                        new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
                right.addView(space(8));
            }
            List<Exercise> list = new ArrayList<Exercise>();
            for (Exercise exercise : allExercises()) {
                if (matchesLibraryFilter(exercise) && matchesLibraryQuery(exercise) && matchesReviewFilter(exercise)) {
                    list.add(exercise);
                }
            }
            if (datasetLoadError.length() > 0) {
                right.addView(text("默认动作数据加载失败：" + datasetLoadError, 12, Typeface.NORMAL, CORAL));
                right.addView(space(6));
            }
            if (list.isEmpty()) {
                right.addView(text(libraryQuery.length() == 0 ? "这个分类还没有动作。"
                        : "没有匹配的动作。", 14, Typeface.NORMAL, MUTED));
            }
            int visibleCount = Math.min(list.size(), libraryVisibleLimit);
            if (!list.isEmpty()) {
                right.addView(text("共 " + list.size() + " 个·当前显示 " + visibleCount + " 个",
                        12, Typeface.NORMAL, MUTED));
                right.addView(space(6));
            }
            for (int i = 0; i < visibleCount; i += 2) {
                LinearLayout row = new LinearLayout(this);
                row.setOrientation(LinearLayout.HORIZONTAL);
                addGridCell(row, list.get(i));
                row.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
                if (i + 1 < visibleCount) {
                    addGridCell(row, list.get(i + 1));
                } else {
                    row.addView(new Space(this), new LinearLayout.LayoutParams(0, 1, 1f));
                }
                right.addView(row);
                right.addView(space(8));
            }
            if (visibleCount < list.size()) {
                int remaining = list.size() - visibleCount;
                right.addView(button("再加载 " + Math.min(60, remaining) + " 个（剩余 " + remaining + "）",
                        Color.rgb(236, 240, 234), INK, v -> {
                            libraryVisibleLimit += 60;
                            renderLibrary(libraryFilter);
                        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
            }
        }
        rightScroll.addView(right);
        pane.addView(rightScroll, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.MATCH_PARENT, 1f));
        content.addView(pane);
        renderBottomNav();
    }

    private List<String> libraryCategories() {
        List<String> categories = new ArrayList<String>();
        categories.add("全部");
        for (String category : Arrays.asList("背", "胸", "腿", "臀", "肩", "核心", "手臂", "有氧", "颈")) {
            if (!deletedCategories.contains(category)) {
                categories.add(category);
            }
        }
        categories.addAll(customRegions());
        categories.add("已标心");
        categories.add("我的动作");
        categories.add("待确认");
        return categories;
    }

    private View sidebarItem(final String category) {
        boolean selected = category.equals(libraryFilter);
        Button item = button(category, selected ? GREEN : SURFACE, selected ? Color.WHITE : MUTED,
                v -> renderLibrary(category));
        item.setTextSize(13);
        if (canDeleteCategory(category)) {
            item.setOnLongClickListener(v -> {
                confirmDeleteCategory(category);
                return true;
            });
        }
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(44));
        lp.setMargins(0, 0, 0, dp(6));
        item.setLayoutParams(lp);
        return item;
    }

    private void addGridCell(LinearLayout row, final Exercise exercise) {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setBackground(bg(SURFACE, dp(14), SURFACE, 0));
        card.setElevation(dp(2));
        card.setPadding(dp(6), dp(6), dp(6), dp(8));
        card.addView(imageThumb(exercise, 132));
        card.addView(space(6));
        TextView name = text(exercise.name(), 13, Typeface.BOLD, INK);
        name.setGravity(Gravity.CENTER);
        name.setMaxLines(2);
        card.addView(name);
        TextView reviewTag = text(reviewLabel(exercise), 11, Typeface.BOLD, isReviewed(exercise) ? GREEN : AMBER);
        reviewTag.setGravity(Gravity.CENTER);
        card.addView(reviewTag);
        if (favoriteIds.contains(exercise.id())) {
            TextView tag = text("♥", 12, Typeface.BOLD, HEART_RED);
            tag.setGravity(Gravity.CENTER);
            card.addView(tag);
        }
        card.setOnClickListener(v -> showExerciseDetail(exercise));
        card.setOnLongClickListener(v -> {
            showExerciseActions(exercise);
            return true;
        });
        row.addView(card, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
    }

    private View imageThumb(final Exercise exercise, int heightDp) {
        final int maximumHeight = dp(heightDp);
        FrameLayout frame = new FrameLayout(this) {
            @Override
            protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
                int width = View.MeasureSpec.getSize(widthMeasureSpec);
                int squareHeight = Math.min(width, maximumHeight);
                super.onMeasure(widthMeasureSpec,
                        View.MeasureSpec.makeMeasureSpec(squareHeight, View.MeasureSpec.EXACTLY));
            }
        };
        frame.setBackground(bg(Color.WHITE, dp(10), Color.rgb(235, 239, 232), 1));
        frame.setLayoutParams(new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        final int radius = dp(10);
        frame.setClipToOutline(true);
        frame.setOutlineProvider(new ViewOutlineProvider() {
            @Override
            public void getOutline(View view, Outline outline) {
                outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), radius);
            }
        });

        String media = effectiveMedia(exercise);
        boolean localReadable = !isLocalUri(media) || canReadLocalMedia(media);
        boolean imageLike = hasEffectiveMedia(exercise)
                && localReadable
                && (isPackagedMedia(media) || isLocalUri(media) || (isWebUrl(media) && isImageUrl(media)));
        if (imageLike) {
            ImageView image = new ImageView(this);
            image.setScaleType(ImageView.ScaleType.FIT_CENTER);
            frame.addView(image, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
            if (isPackagedMedia(media)) {
                loadPackagedImage(image, media, 320, true);
            } else {
                loadThumbInto(image, media);
            }
        } else {
            TextView missing = text(hasEffectiveMedia(exercise) ? "打开动作来源" : "暂无示范\n待补图", 13, Typeface.NORMAL, MUTED);
            missing.setGravity(Gravity.CENTER);
            frame.addView(missing, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        }

        TextView tag = text(exercise.targetRegions().isEmpty() ? "" : exercise.targetRegions().get(0),
                10, Typeface.BOLD, GREEN);
        tag.setPadding(dp(5), dp(2), dp(5), dp(2));
        tag.setBackground(bg(GREEN_SOFT, dp(6), GREEN_SOFT, 0));
        FrameLayout.LayoutParams tlp = new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        tlp.gravity = Gravity.TOP | Gravity.LEFT;
        tlp.setMargins(dp(6), dp(5), 0, 0);
        frame.addView(tag, tlp);
        return frame;
    }

    private void loadThumbInto(final ImageView image, final String url) {
        Bitmap cached = thumbCache.get(url);
        if (cached != null) {
            image.setImageBitmap(cached);
            return;
        }
        image.setTag(url);
        new Thread(new Runnable() {
            @Override
            public void run() {
                final Bitmap bitmap = decodeThumb(url);
                if (bitmap == null) {
                    return;
                }
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        thumbCache.put(url, bitmap);
                        if (url.equals(image.getTag())) {
                            image.setImageBitmap(bitmap);
                        }
                    }
                });
            }
        }).start();
    }

    private Bitmap decodeThumb(String url) {
        try {
            byte[] data;
            if (isLocalUri(url)) {
                java.io.InputStream is = openLocalMedia(Uri.parse(url));
                if (is == null) return null;
                data = readAllBytes(is);
                is.close();
            } else {
                java.net.HttpURLConnection conn = (java.net.HttpURLConnection) new java.net.URL(url).openConnection();
                conn.setConnectTimeout(8000);
                conn.setReadTimeout(8000);
                conn.setInstanceFollowRedirects(true);
                conn.connect();
                java.io.InputStream is = conn.getInputStream();
                data = readAllBytes(is);
                is.close();
                conn.disconnect();
            }
            BitmapFactory.Options bounds = new BitmapFactory.Options();
            bounds.inJustDecodeBounds = true;
            BitmapFactory.decodeByteArray(data, 0, data.length, bounds);
            int sample = 1;
            int max = Math.max(bounds.outWidth, bounds.outHeight);
            while (max / sample > 420) {
                sample *= 2;
            }
            BitmapFactory.Options opts = new BitmapFactory.Options();
            opts.inSampleSize = sample;
            return BitmapFactory.decodeByteArray(data, 0, data.length, opts);
        } catch (Exception ignored) {
            return null;
        }
    }

    private byte[] readAllBytes(java.io.InputStream is) throws java.io.IOException {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        byte[] buffer = new byte[8192];
        int read;
        while ((read = is.read(buffer)) != -1) {
            out.write(buffer, 0, read);
        }
        return out.toByteArray();
    }

    private List<String> customRegions() {
        Set<String> builtin = new HashSet<String>(Arrays.asList(
                "背", "胸", "腿", "臀", "肩", "核心", "手臂", "有氧", "颈"));
        LinkedHashSet<String> result = new LinkedHashSet<String>();
        for (Exercise exercise : allExercises()) {
            for (String region : exercise.targetRegions()) {
                if (!builtin.contains(region) && !deletedCategories.contains(region)) {
                    result.add(region);
                }
            }
        }
        return new ArrayList<String>(result);
    }

    private boolean canDeleteCategory(String category) {
        return category != null
                && category.length() > 0
                && !"全部".equals(category)
                && !"已标心".equals(category)
                && !"我的动作".equals(category)
                && !"待确认".equals(category)
                && !deletedCategories.contains(category);
    }

    private void confirmDeleteCategory(final String category) {
        if (!canDeleteCategory(category)) {
            return;
        }
        new AlertDialog.Builder(this)
                .setTitle("删除分类？")
                .setMessage("会删除「" + category + "」这个分类入口，动作本身仍保留在全部和我的动作里。")
                .setNegativeButton("取消", null)
                .setPositiveButton("删除", (dialog, which) -> {
                    deletedCategories.add(category);
                    saveState();
                    Toast.makeText(this, "已删除分类「" + category + "」", Toast.LENGTH_SHORT).show();
                    renderLibrary("全部");
                })
                .show();
    }

    private void showExerciseActions(final Exercise exercise) {
        final String[] items = new String[]{"查看详情", "编辑", "删除动作"};
        new AlertDialog.Builder(this)
                .setTitle(exercise.name())
                .setItems(items, (dialog, which) -> {
                    if (which == 0) {
                        showExerciseDetail(exercise);
                    } else if (which == 1) {
                        editExercise(exercise);
                    } else {
                        confirmDeleteExercise(exercise, null);
                    }
                })
                .show();
    }

    private void confirmDeleteExercise(final Exercise exercise, final AlertDialog owner) {
        if (inSession && activePlanContains(exercise.id())) {
            Toast.makeText(this, "这个动作在暂存训练中，请结束本次训练后再删除。", Toast.LENGTH_LONG).show();
            return;
        }
        String message = isCustomExercise(exercise)
                ? "删除后无法恢复。"
                : "这个内置动作会从本机动作库和自动推荐中隐藏。";
        new AlertDialog.Builder(this)
                .setTitle("删除动作？")
                .setMessage(message)
                .setNegativeButton("取消", null)
                .setPositiveButton("删除", (dialog, which) -> {
                    deleteExercise(exercise);
                    if (owner != null) {
                        owner.dismiss();
                    }
                    Toast.makeText(this, "已删除动作「" + exercise.name() + "」", Toast.LENGTH_SHORT).show();
                    renderLibrary(deletedCategories.contains(libraryFilter) ? "全部" : libraryFilter);
                })
                .show();
    }

    private void deleteExercise(Exercise exercise) {
        String id = exercise.id();
        if (isCustomExercise(exercise)) {
            for (int i = customExercises.size() - 1; i >= 0; i--) {
                if (customExercises.get(i).id().equals(id)) {
                    customExercises.remove(i);
                }
            }
        } else {
            deletedExerciseIds.add(id);
        }
        favoriteIds.remove(id);
        verifiedIds.remove(id);
        mediaOverrides.remove(id);
        if (activePlanContains(id)) {
            currentPlan = null;
            activeItems.clear();
            inSession = false;
        }
        saveState();
    }

    private boolean activePlanContains(String exerciseId) {
        for (WorkoutItem item : activeItems) {
            if (item.exercise().id().equals(exerciseId)) {
                return true;
            }
        }
        return false;
    }

    private void addPendingShares(LinearLayout target) {
        if (pendingShares.isEmpty()) {
            LinearLayout empty = card();
            empty.addView(section("待确认动作"));
            empty.addView(text("还没有从外部 App 分享进来的动作。", 14, Typeface.NORMAL, MUTED));
            target.addView(empty);
            return;
        }
        for (int i = 0; i < pendingShares.size(); i++) {
            PendingShare share = pendingShares.get(i);
            LinearLayout card = card();
            card.addView(section(share.title));
            card.addView(text(share.createdAt + " · 来源已保留", 13, Typeface.NORMAL, MUTED));
            if (share.body.length() > 0) {
                card.addView(text(share.body, 14, Typeface.NORMAL, INK));
            }
            if (share.uri.length() > 0) {
                card.addView(text(share.uri, 13, Typeface.NORMAL, BLUE));
            }
            final int index = i;
            card.addView(space(10));
            card.addView(button("确认入库为未验证动作", GREEN, Color.WHITE, v -> confirmPendingShare(index)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
            target.addView(card);
        }
    }

    private void confirmPendingShare(int index) {
        if (index < 0 || index >= pendingShares.size()) {
            return;
        }
        PendingShare share = pendingShares.remove(index);
        boolean bodyIsLink = isWebUrl(share.body);
        String media;
        if (isWebUrl(share.uri) || isLocalUri(share.uri)) {
            media = share.uri;
        } else if (bodyIsLink) {
            media = share.body;
        } else {
            media = "";
        }
        String instruction = (share.body.length() == 0 || bodyIsLink)
                ? "外部分享素材，待补充动作步骤。" : share.body;
        customExercises.add(customExercise("custom_share_" + System.currentTimeMillis(),
                share.title, new ArrayList<String>(Arrays.asList("背")), instruction, media));
        saveState();
        Toast.makeText(this, "已进入我的动作，状态为未验证", Toast.LENGTH_SHORT).show();
        renderLibrary("我的动作");
    }

    private EvidenceStatus effectiveStatus(Exercise exercise) {
        if (exercise.evidenceStatus() == EvidenceStatus.USER_UNVERIFIED && verifiedIds.contains(exercise.id())) {
            return EvidenceStatus.EXPERT_REVIEWED;
        }
        return exercise.evidenceStatus();
    }

    private void toggleVerified(Exercise exercise) {
        if (verifiedIds.contains(exercise.id())) {
            verifiedIds.remove(exercise.id());
            Toast.makeText(this, "已撤销验证，恢复为未验证", Toast.LENGTH_SHORT).show();
        } else {
            verifiedIds.add(exercise.id());
            Toast.makeText(this, "已标记为已验证，可进入自动推荐", Toast.LENGTH_SHORT).show();
        }
        saveState();
        renderLibrary(libraryFilter);
    }

    private void editExercise(Exercise exercise) {
        if (isCustomExercise(exercise)) {
            showCustomForm(exercise);
        } else {
            showEditMediaDialog(exercise);
        }
    }

    private boolean isCustomExercise(Exercise exercise) {
        for (Exercise custom : customExercises) {
            if (custom.id().equals(exercise.id())) {
                return true;
            }
        }
        return false;
    }

    private void replaceCustomExercise(String id, Exercise updated) {
        for (int i = 0; i < customExercises.size(); i++) {
            if (customExercises.get(i).id().equals(id)) {
                customExercises.set(i, updated);
                return;
            }
        }
    }

    /** 自定义动作选择一个主要器械；单选与推荐引擎“任一器械可用”的既有语义保持一致。 */
    private Spinner customEquipmentPicker(List<String> selected) {
        List<String> options = equipmentOptions();
        if (selected != null) {
            for (String item : selected) {
                if (item != null && item.length() > 0 && !options.contains(item)) {
                    options.add(item);
                }
            }
        }
        Spinner picker = new Spinner(this);
        picker.setContentDescription("器械选择");
        android.widget.ArrayAdapter<String> adapter = new android.widget.ArrayAdapter<String>(
                this, android.R.layout.simple_spinner_item, options);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        picker.setAdapter(adapter);
        String current = selected == null || selected.isEmpty() ? "自重" : selected.get(0);
        int at = options.indexOf(current);
        picker.setSelection(at < 0 ? 0 : at);
        return picker;
    }

    private void showCustomForm(final Exercise existing) {
        final boolean editing = existing != null;
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));

        final EditText name = new EditText(this);
        name.setHint("动作名称");
        name.setSingleLine(true);
        if (editing) {
            name.setText(existing.name());
        }
        box.addView(name);

        box.addView(space(6));
        box.addView(text("分类（可多选，部位和自定义分类是一回事）", 13, Typeface.BOLD, MUTED));
        final List<String> currentRegions = editing ? existing.targetRegions() : new ArrayList<String>();
        final List<String> categories = new ArrayList<String>();
        for (String region : Arrays.asList("背", "胸", "腿", "肩", "核心", "手臂")) {
            categories.add(region);
        }
        for (String custom : customRegions()) {
            if (!categories.contains(custom)) {
                categories.add(custom);
            }
        }
        for (String region : currentRegions) {
            if (!categories.contains(region)) {
                categories.add(region);
            }
        }
        final List<CheckBox> categoryBoxes = new ArrayList<CheckBox>();
        LinearLayout catWrap = new LinearLayout(this);
        catWrap.setOrientation(LinearLayout.HORIZONTAL);
        for (String category : categories) {
            CheckBox box2 = new CheckBox(this);
            box2.setText(category);
            box2.setTextColor(INK);
            box2.setChecked(currentRegions.contains(category));
            categoryBoxes.add(box2);
            catWrap.addView(box2);
        }
        HorizontalScrollView regionScroll = new HorizontalScrollView(this);
        regionScroll.setHorizontalScrollBarEnabled(false);
        regionScroll.addView(catWrap);
        box.addView(regionScroll);

        final EditText newGroup = new EditText(this);
        newGroup.setHint("新建分类（如：足球、瑜伽）；填了会一起加上");
        newGroup.setSingleLine(true);
        box.addView(newGroup);

        box.addView(space(8));
        box.addView(text("器械（单选，可随时修改）", 13, Typeface.BOLD, MUTED));
        final Spinner equipmentPicker = customEquipmentPicker(
                editing ? existing.equipment() : new ArrayList<String>(Arrays.asList("自重")));
        box.addView(equipmentPicker, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));

        box.addView(space(6));
        box.addView(text("示范图 / 视频", 13, Typeface.BOLD, MUTED));
        final EditText media = new EditText(this);
        media.setHint("粘贴链接，或点下面按钮从相册选");
        media.setSingleLine(true);
        if (editing) {
            media.setText(effectiveMedia(existing));
        }
        box.addView(media);
        box.addView(button("从相册 / 文件选择图片", Color.rgb(236, 240, 234), INK, v -> pickLocalImage(media)),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        box.addView(text("图片或 GIF 会复制到 App 内保存，不再依赖相册的临时链接。",
                12, Typeface.NORMAL, MUTED));

        box.addView(space(8));
        box.addView(text("动作要点（每行一条，会分条显示）", 13, Typeface.BOLD, MUTED));
        final EditText description = new EditText(this);
        description.setHint("例如：\n双脚与肩同宽\n核心收紧，背部保持中立\n呼气发力，吸气还原");
        description.setMinLines(6);
        description.setGravity(Gravity.TOP | Gravity.START);
        description.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        description.setBackground(bg(Color.rgb(249, 251, 247), dp(8), LINE, 1));
        description.setPadding(dp(12), dp(10), dp(12), dp(10));
        if (editing && !existing.instructions().isEmpty()) {
            StringBuilder joined = new StringBuilder();
            for (String line : existing.instructions()) {
                if (joined.length() > 0) {
                    joined.append("\n");
                }
                joined.append(line);
            }
            description.setText(joined.toString());
        }
        LinearLayout.LayoutParams descLp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(150));
        descLp.setMargins(0, dp(4), 0, 0);
        box.addView(description, descLp);

        ScrollView scroll = new ScrollView(this);
        scroll.addView(box);
        new AlertDialog.Builder(this)
                .setTitle(editing ? "编辑动作" : "新增动作")
                .setView(scroll)
                .setNegativeButton("取消", null)
                .setPositiveButton("保存", (dialog, which) -> {
                    String actionName = name.getText().toString().trim();
                    if (actionName.length() == 0) {
                        Toast.makeText(this, "动作名称不能为空", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    List<String> chosen = new ArrayList<String>();
                    for (CheckBox box2 : categoryBoxes) {
                        if (box2.isChecked()) {
                            chosen.add(box2.getText().toString());
                        }
                    }
                    String typed = newGroup.getText().toString().trim();
                    if (typed.length() > 0 && !chosen.contains(typed)) {
                        chosen.add(typed);
                    }
                    if (chosen.isEmpty()) {
                        Toast.makeText(this, "请至少选择或新建一个分类", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    String body = description.getText().toString().trim();
                    String mediaUrl = media.getText().toString().trim();
                    String id = editing ? existing.id() : "custom_manual_" + System.currentTimeMillis();
                    Exercise updated = customExercise(id, actionName, chosen,
                            body.length() == 0 ? "用户自定义动作，待补充步骤。" : body, mediaUrl,
                            Arrays.asList(String.valueOf(equipmentPicker.getSelectedItem())));
                    if (editing) {
                        replaceCustomExercise(id, updated);
                        mediaOverrides.remove(id);
                    } else {
                        customExercises.add(updated);
                    }
                    saveState();
                    Toast.makeText(this, editing ? "已更新动作" : "已新增到「" + chosen.get(0) + "」，状态为未验证",
                            Toast.LENGTH_SHORT).show();
                    renderLibrary(chosen.get(0));
                })
                .show();
    }

    private void showEditMediaDialog(final Exercise exercise) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));
        box.addView(text("内置动作的名称和步骤是固定的，这里可以替换或自定义示范图。",
                13, Typeface.NORMAL, MUTED));
        box.addView(space(8));
        final EditText media = new EditText(this);
        media.setHint("粘贴图片 / 视频链接，或从相册选");
        media.setText(effectiveMedia(exercise));
        media.setSingleLine(true);
        box.addView(media);
        box.addView(button("从相册 / 文件选择图片", Color.rgb(236, 240, 234), INK, v -> pickLocalImage(media)),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        box.addView(text("图片或 GIF 会复制到 App 内保存，不再依赖相册的临时链接。",
                12, Typeface.NORMAL, MUTED));

        new AlertDialog.Builder(this)
                .setTitle("编辑示范图 · " + exercise.name())
                .setView(box)
                .setNegativeButton("取消", null)
                .setNeutralButton("恢复默认", (dialog, which) -> {
                    mediaOverrides.remove(exercise.id());
                    saveState();
                    Toast.makeText(this, "已恢复默认示范图", Toast.LENGTH_SHORT).show();
                    renderLibrary(libraryFilter);
                })
                .setPositiveButton("保存", (dialog, which) -> {
                    String url = media.getText().toString().trim();
                    if (url.length() == 0 || url.equals(exercise.media())) {
                        mediaOverrides.remove(exercise.id());
                    } else {
                        mediaOverrides.put(exercise.id(), url);
                    }
                    saveState();
                    Toast.makeText(this, "已更新示范图", Toast.LENGTH_SHORT).show();
                    renderLibrary(libraryFilter);
                })
                .show();
    }

    private void pickLocalImage(EditText target) {
        pendingMediaField = target;
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("image/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION
                    | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
            startActivityForResult(intent, REQ_PICK_MEDIA);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开图片选择器", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQ_UPDATE_INSTALL_PERMISSION) {
            if (getPackageManager().canRequestPackageInstalls() && pendingUpdateApk != null) {
                launchUpdateInstaller(pendingUpdateApk);
            } else {
                setGitHubUpdateStatus("尚未允许安装更新；授权后可点“安装已下载更新”", false);
            }
            return;
        }
        if (requestCode == REQ_PICK_MEDIA && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            Uri uri = data.getData();
            try {
                String stored = importExerciseMedia(uri);
                if (pendingMediaField != null) {
                    pendingMediaField.setText(stored);
                    Toast.makeText(this, "已复制到 App，图片或 GIF 之后仍可打开", Toast.LENGTH_LONG).show();
                }
            } catch (Exception error) {
                Toast.makeText(this, "图片未能保存，请重新选择", Toast.LENGTH_LONG).show();
            } finally {
                pendingMediaField = null;
            }
        } else if (requestCode == REQ_EXPORT_BACKUP && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            writeBackupFile(data.getData());
        } else if (requestCode == REQ_IMPORT_BACKUP && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            importBackupFile(data.getData());
        } else if (requestCode == REQ_PICK_RECIPE_IMPORT && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            Uri uri = persistUri(data.getData());
            importRecipeFromImage(uri);
        } else if (requestCode == REQ_PICK_RECIPE_PHOTO && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            Uri uri = persistUri(data.getData());
            addRecipePhoto(pendingRecipePhotoId, uri.toString());
            pendingRecipePhotoId = null;
        } else if (requestCode == REQ_PICK_RECIPE_COVER && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            Uri uri = persistUri(data.getData());
            if (editorDraft != null) {
                harvestEditor();
                editorDraft.sourceMedia = uri.toString();
                renderRecipeEditor();
            }
        } else if (requestCode == REQ_PICK_MEAL_PHOTO && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            estimateMealFromImage(persistUri(data.getData()));
        } else if (requestCode == REQ_PICK_STEP_IMAGE && resultCode == RESULT_OK
                && data != null && data.getData() != null) {
            Uri uri = persistUri(data.getData());
            if (editorDraft != null && pendingStepIndex >= 0 && pendingStepIndex < editorDraft.steps.size()) {
                harvestEditor();
                editorDraft.steps.get(pendingStepIndex).image = uri.toString();
                renderRecipeEditor();
            }
            pendingStepIndex = -1;
        }
    }

    /**
     * 相册提供的 content:// 许可可能在重启、清理相册或提供方变化后失效。
     * 动作示范体积可控，选择时直接复制进 App 私有目录，保存稳定的 file:// 地址。
     */
    private String importExerciseMedia(Uri source) throws java.io.IOException {
        File directory = new File(getFilesDir(), "exercise_media");
        if (!directory.exists() && !directory.mkdirs()) {
            throw new java.io.IOException("Cannot create exercise media directory");
        }
        String extension = exerciseMediaExtension(source);
        File target = new File(directory, "motion_" + java.util.UUID.randomUUID() + "." + extension);
        InputStream input = null;
        FileOutputStream output = null;
        boolean complete = false;
        try {
            input = "file".equalsIgnoreCase(source.getScheme())
                    ? new FileInputStream(new File(source.getPath()))
                    : getContentResolver().openInputStream(source);
            if (input == null) throw new java.io.IOException("Cannot open selected media");
            output = new FileOutputStream(target);
            byte[] buffer = new byte[8192];
            long total = 0;
            int read;
            while ((read = input.read(buffer)) != -1) {
                total += read;
                if (total > 100L * 1024L * 1024L) {
                    throw new java.io.IOException("Exercise media exceeds 100 MB");
                }
                output.write(buffer, 0, read);
            }
            output.flush();
            if (total == 0) throw new java.io.IOException("Selected media is empty");
            complete = true;
            return Uri.fromFile(target).toString();
        } finally {
            if (input != null) try { input.close(); } catch (Exception ignored) {}
            if (output != null) try { output.close(); } catch (Exception ignored) {}
            if (!complete && target.exists()) target.delete();
        }
    }

    private String exerciseMediaExtension(Uri source) {
        String extension = "";
        try {
            String mime = getContentResolver().getType(source);
            extension = MimeTypeMap.getSingleton().getExtensionFromMimeType(mime);
        } catch (Exception ignored) {}
        if (extension == null || extension.length() == 0) {
            String name = "";
            Cursor cursor = null;
            try {
                cursor = getContentResolver().query(source,
                        new String[]{OpenableColumns.DISPLAY_NAME}, null, null, null);
                if (cursor != null && cursor.moveToFirst()) name = cursor.getString(0);
            } catch (Exception ignored) {
            } finally {
                if (cursor != null) cursor.close();
            }
            int dot = name.lastIndexOf('.');
            if (dot >= 0 && dot < name.length() - 1) extension = name.substring(dot + 1);
        }
        extension = extension == null ? "img" : extension.toLowerCase(Locale.ROOT);
        return extension.matches("[a-z0-9]{1,6}") ? extension : "img";
    }

    private Uri persistUri(Uri uri) {
        try {
            getContentResolver().takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION);
        } catch (Exception ignored) {
            // Some providers don't grant persistable permission; the URI may still work this session.
        }
        return uri;
    }

    private void addRecipePhoto(String recipeId, String url) {
        Recipe recipe = recipeById(recipeId);
        if (recipe == null || url == null || url.length() == 0) {
            return;
        }
        recipe.photos.add(url);
        saveState();
        Toast.makeText(this, "已添加成品照", Toast.LENGTH_SHORT).show();
        if ("food".equals(currentTab)) {
            if (recipe.id.equals(currentRecipeId)) {
                renderRecipeDetail(recipe);
            } else {
                renderFood();
            }
        }
    }

    private void startBackupExport() {
        try {
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/json");
            String stamp = new SimpleDateFormat("yyyyMMdd", Locale.CHINA).format(new Date());
            intent.putExtra(Intent.EXTRA_TITLE, "健身记录备份-" + stamp + ".json");
            startActivityForResult(intent, REQ_EXPORT_BACKUP);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开文件保存器", Toast.LENGTH_SHORT).show();
        }
    }

    private void startBackupImport() {
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("*/*");
            intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{
                    "application/json", "text/plain", "application/octet-stream"});
            startActivityForResult(intent, REQ_IMPORT_BACKUP);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开文件选择器", Toast.LENGTH_SHORT).show();
        }
    }

    private void writeBackupFile(Uri uri) {
        try {
            JSONObject root = new JSONObject();
            root.put("app", "restartday-fitness");
            root.put("type", "records-backup");
            root.put("version", 3);
            root.put("exportedAt", System.currentTimeMillis());
            root.put("records", recordsJson());
            root.put("recipes", recipesJson());
            OutputStream out = getContentResolver().openOutputStream(uri);
            try {
                out.write(root.toString(2).getBytes(StandardCharsets.UTF_8));
            } finally {
                out.close();
            }
            Toast.makeText(this, "已备份 " + trainingRecords.size() + " 条训练记录、"
                    + recipes.size() + " 个菜谱", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Toast.makeText(this, "备份失败：" + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void importBackupFile(Uri uri) {
        String text;
        try {
            InputStream in = getContentResolver().openInputStream(uri);
            try {
                ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                byte[] chunk = new byte[8192];
                int read;
                while ((read = in.read(chunk)) != -1) {
                    buffer.write(chunk, 0, read);
                    if (buffer.size() > 8 * 1024 * 1024) {
                        Toast.makeText(this, "文件太大，不像是记录备份", Toast.LENGTH_LONG).show();
                        return;
                    }
                }
                text = new String(buffer.toByteArray(), StandardCharsets.UTF_8).trim();
            } finally {
                in.close();
            }
        } catch (Exception e) {
            Toast.makeText(this, "读取文件失败：" + e.getMessage(), Toast.LENGTH_LONG).show();
            return;
        }

        JSONArray array = null;
        JSONArray recipeArray = null;
        try {
            if (text.startsWith("[")) {
                array = new JSONArray(text);
            } else {
                JSONObject root = new JSONObject(text);
                array = root.optJSONArray("records");
                recipeArray = root.optJSONArray("recipes");
            }
        } catch (Exception ignored) {
            // Fall through to the error toast below.
        }
        if (array == null && recipeArray == null) {
            Toast.makeText(this, "无法识别的备份格式，需要本 App 导出的 JSON 备份文件", Toast.LENGTH_LONG).show();
            return;
        }

        Set<String> existing = new HashSet<String>();
        for (SessionRecord record : trainingRecords) {
            existing.add(recordKey(record));
        }
        int added = 0;
        int skipped = 0;
        if (array != null) {
            for (int i = 0; i < array.length(); i++) {
                JSONObject object = array.optJSONObject(i);
                if (object == null) {
                    continue;
                }
                SessionRecord record = recordFromJson(object);
                if (record.time.length() == 0 && record.title.length() == 0 && record.epochMillis == 0) {
                    continue;
                }
                if (existing.add(recordKey(record))) {
                    trainingRecords.add(record);
                    added++;
                } else {
                    skipped++;
                }
            }
        }

        int recipesAdded = importRecipesFromJson(recipeArray);

        if (added > 0 || recipesAdded > 0) {
            if (added > 0) {
                Collections.sort(trainingRecords, (a, b) -> Long.compare(b.epochMillis, a.epochMillis));
            }
            saveState();
        }
        StringBuilder message = new StringBuilder();
        if (added > 0) {
            message.append("已导入 ").append(added).append(" 条记录");
            if (skipped > 0) {
                message.append("（跳过重复 ").append(skipped).append(" 条）");
            }
        } else if (skipped > 0) {
            message.append("训练记录全部 ").append(skipped).append(" 条都已存在");
        }
        if (recipesAdded > 0) {
            if (message.length() > 0) {
                message.append("；");
            }
            message.append("导入 ").append(recipesAdded).append(" 个菜谱");
        }
        if (message.length() == 0) {
            message.append("文件里没有可导入的新内容");
        }
        Toast.makeText(this, message.toString(), Toast.LENGTH_LONG).show();
        if (added > 0) {
            renderRecords();
        } else if (recipesAdded > 0) {
            renderFood();
        }
    }

    private int importRecipesFromJson(JSONArray recipeArray) {
        if (recipeArray == null) {
            return 0;
        }
        Set<String> existingIds = new HashSet<String>();
        Set<String> existingNames = new HashSet<String>();
        for (Recipe recipe : recipes) {
            existingIds.add(recipe.id);
            existingNames.add(recipe.name);
        }
        int recipesAdded = 0;
        for (int i = 0; i < recipeArray.length(); i++) {
            JSONObject object = recipeArray.optJSONObject(i);
            if (object == null) {
                continue;
            }
            Recipe recipe = recipeFromJson(object, i);
            if (recipe.name.length() == 0) {
                continue;
            }
            if (existingIds.contains(recipe.id) || existingNames.contains(recipe.name)) {
                continue;
            }
            existingIds.add(recipe.id);
            existingNames.add(recipe.name);
            recipes.add(recipe);
            recipesAdded++;
        }
        return recipesAdded;
    }

    private String recordKey(SessionRecord record) {
        if (record.epochMillis > 0) {
            return "e" + record.epochMillis;
        }
        return record.time + "|" + record.title + "|" + record.duration;
    }

    private int recordIndexByKey(String key) {
        for (int i = 0; i < trainingRecords.size(); i++) {
            if (recordKey(trainingRecords.get(i)).equals(key)) {
                return i;
            }
        }
        return -1;
    }

    private boolean healthSupported() {
        return Build.VERSION.SDK_INT >= 34 && getSystemService("healthconnect") != null;
    }

    private boolean healthPermissionGranted() {
        if (Build.VERSION.SDK_INT < 34) return false;
        for (String p : HEALTH_PERMISSIONS) if (!p.equals(HEALTH_READ_EXERCISE)
                && checkSelfPermission(p) == PackageManager.PERMISSION_GRANTED) return true;
        return false;
    }

    private boolean allHealthPermissionsGranted() {
        if (Build.VERSION.SDK_INT < 34) return false;
        for (String p : HEALTH_PERMISSIONS) if (checkSelfPermission(p) != PackageManager.PERMISSION_GRANTED) return false;
        return true;
    }

    private void syncHeartRateForRecord(String key, boolean silent) {
        if (!healthSupported()) {
            if (!silent) Toast.makeText(this, "手表数据同步需要 Android 14 及以上的健康连接", Toast.LENGTH_LONG).show();
            return;
        }
        int index = recordIndexByKey(key);
        if (index < 0 || trainingRecords.get(index).epochMillis <= 0) return;
        if (!silent && !allHealthPermissionsGranted()) {
            pendingHeartRateRecordKey = key; requestPermissions(HEALTH_PERMISSIONS, REQ_HEALTH_PERMISSION); return;
        }
        if (healthPermissionGranted()) readHeartRate(key, silent);
    }

    /**
     * 先看手表自己有没有写「运动记录」：有就用它的起止作为权威窗口，两边数字才可能真正对上；
     * 没有（或没授权读运动记录）就退回本机计时的窗口。
     */
    private void readHeartRate(final String key, final boolean silent) {
        int index = recordIndexByKey(key);
        if (index < 0) {
            return;
        }
        SessionRecord record = trainingRecords.get(index);
        Object service = getSystemService("healthconnect");
        if (!(service instanceof android.health.connect.HealthConnectManager)) {
            if (!silent) {
                Toast.makeText(this, "此手机没有健康连接（Health Connect）服务", Toast.LENGTH_LONG).show();
            }
            return;
        }
        final android.health.connect.HealthConnectManager manager =
                (android.health.connect.HealthConnectManager) service;
        final long localStart = record.windowStartMillis(durationSeconds(record.duration));
        final long localEnd = record.epochMillis;
        if (localEnd <= localStart) {
            return;
        }
        if (checkSelfPermission(HEALTH_READ_EXERCISE) != PackageManager.PERMISSION_GRANTED) {
            readHeartRateWindow(manager, key, localStart, localEnd, "", silent);
            return;
        }
        try {
            android.health.connect.ReadRecordsRequestUsingFilters<android.health.connect.datatypes.ExerciseSessionRecord> request =
                    new android.health.connect.ReadRecordsRequestUsingFilters.Builder<>(
                            android.health.connect.datatypes.ExerciseSessionRecord.class)
                            .setTimeRangeFilter(rangeFilter(localStart - SESSION_MATCH_SLACK_MS,
                                    localEnd + SESSION_MATCH_SLACK_MS))
                            .build();
            manager.readRecords(request, getMainExecutor(),
                    new OutcomeReceiver<android.health.connect.ReadRecordsResponse<android.health.connect.datatypes.ExerciseSessionRecord>,
                            android.health.connect.HealthConnectException>() {
                        @Override
                        public void onResult(android.health.connect.ReadRecordsResponse<android.health.connect.datatypes.ExerciseSessionRecord> response) {
                            android.health.connect.datatypes.ExerciseSessionRecord best =
                                    bestOverlappingSession(response.getRecords(), localStart, localEnd);
                            if (best == null) {
                                readHeartRateWindow(manager, key, localStart, localEnd, "", silent);
                                return;
                            }
                            readHeartRateWindow(manager, key,
                                    best.getStartTime().toEpochMilli(),
                                    best.getEndTime().toEpochMilli(),
                                    watchSessionLabel(best), best.getMetadata().getDataOrigin().getPackageName(), silent);
                        }

                        @Override
                        public void onError(android.health.connect.HealthConnectException error) {
                            readHeartRateWindow(manager, key, localStart, localEnd, "", silent);
                        }
                    });
        } catch (Exception ignored) {
            readHeartRateWindow(manager, key, localStart, localEnd, "", silent);
        }
    }

    private void readHeartRateWindow(android.health.connect.HealthConnectManager manager,
            String key, long start, long end, String label, boolean silent) {
        readHeartRateWindow(manager, key, start, end, label, "", silent);
    }

    private void readHeartRateWindow(android.health.connect.HealthConnectManager manager,
            final String key, final long startMs, final long endMs,
            final String watchSession, final String origin, final boolean silent) {
        new WatchMetricsReader(this, manager, startMs, endMs, origin, metrics -> {
            int index = recordIndexByKey(key); if (index < 0) return;
            SessionRecord record = trainingRecords.get(index);
            try {
                for (String metric : new String[]{"activeKcal", "totalKcal", "steps", "distanceM"}) {
                    if (metrics.has(metric)) record.metrics.put(metric, metrics.get(metric));
                }
                record.metrics.put("lastSync", System.currentTimeMillis());
                record.metrics.put("windowLabel", watchSession.isEmpty() ? "本次训练时间段" : watchSession);
            } catch (Exception ignored) { }
            saveState();
            if ("records".equals(currentTab) && !inSession) renderRecords();
            if (!silent) {
                String message = metrics.has("activeKcal") || metrics.has("totalKcal") ? "已同步手表运动数据" :
                        "本次未读到热量；请确认已授权热量，并在手表配套 App 完成同步后重试";
                if (metrics.has("activeKcalError") || metrics.has("totalKcalError")) message = "热量读取失败，已保留原数据；可稍后重试";
                Toast.makeText(this, message, Toast.LENGTH_LONG).show();
            }
        }).read();
        if (checkSelfPermission(HEALTH_READ_HEART_RATE) != PackageManager.PERMISSION_GRANTED) return;
        readHeartRatePage(manager, key, startMs, endMs, watchSession, origin, -1,
                new ArrayList<android.health.connect.datatypes.HeartRateRecord>(), silent);
    }

    private void readHeartRatePage(android.health.connect.HealthConnectManager manager, String key, long startMs, long endMs,
            String label, String origin, long pageToken, List<android.health.connect.datatypes.HeartRateRecord> records, boolean silent) {
        try {
            android.health.connect.ReadRecordsRequestUsingFilters.Builder<android.health.connect.datatypes.HeartRateRecord> builder =
                    new android.health.connect.ReadRecordsRequestUsingFilters.Builder<>(android.health.connect.datatypes.HeartRateRecord.class)
                            .setTimeRangeFilter(rangeFilter(startMs - HR_QUERY_SLACK_MS, endMs + HR_QUERY_SLACK_MS)).setPageSize(1000);
            if (!origin.isEmpty()) builder.addDataOrigins(new android.health.connect.datatypes.DataOrigin.Builder().setPackageName(origin).build());
            if (pageToken >= 0) builder.setPageToken(pageToken);
            manager.readRecords(builder.build(), getMainExecutor(),
                    new OutcomeReceiver<android.health.connect.ReadRecordsResponse<android.health.connect.datatypes.HeartRateRecord>, android.health.connect.HealthConnectException>() {
                        public void onResult(android.health.connect.ReadRecordsResponse<android.health.connect.datatypes.HeartRateRecord> response) {
                            records.addAll(response.getRecords());
                            if (response.getNextPageToken() != -1) {
                                readHeartRatePage(manager, key, startMs, endMs, label, origin, response.getNextPageToken(), records, silent); return;
                            }
                            applyHeartRate(key, records, startMs, endMs, label, silent);
                        }
                        public void onError(android.health.connect.HealthConnectException error) {
                            if (!silent) Toast.makeText(MainActivity.this, "心率读取失败，可稍后重试", Toast.LENGTH_LONG).show();
                        }
                    });
        } catch (Exception e) { if (!silent) Toast.makeText(this, "心率读取失败，可稍后重试", Toast.LENGTH_LONG).show(); }
    }

    private android.health.connect.TimeInstantRangeFilter rangeFilter(long startMs, long endMs) {
        return new android.health.connect.TimeInstantRangeFilter.Builder()
                .setStartTime(Instant.ofEpochMilli(startMs))
                .setEndTime(Instant.ofEpochMilli(endMs))
                .build();
    }

    /** 与本机训练窗口重叠最多的那条手表运动记录。 */
    private android.health.connect.datatypes.ExerciseSessionRecord bestOverlappingSession(
            List<android.health.connect.datatypes.ExerciseSessionRecord> sessions,
            long startMs, long endMs) {
        android.health.connect.datatypes.ExerciseSessionRecord best = null;
        double bestScore = 0;
        for (android.health.connect.datatypes.ExerciseSessionRecord session : sessions) {
            long from = session.getStartTime().toEpochMilli(), to = session.getEndTime().toEpochMilli();
            long overlap = Math.min(endMs, to) - Math.max(startMs, from);
            long localLength = endMs - startMs, watchLength = to - from;
            if (overlap < Math.min(MIN_SESSION_OVERLAP_MS, localLength / 2) || watchLength <= 0 || localLength <= 0
                    || overlap < localLength * .5 || overlap < watchLength * .5) continue;
            double score = overlap * 2.0 / (localLength + watchLength);
            if (score > bestScore) { bestScore = score; best = session; }
        }
        return best;
    }

    private String watchSessionLabel(android.health.connect.datatypes.ExerciseSessionRecord session) {
        String title = session.getTitle() == null ? "" : session.getTitle().toString();
        String time = new SimpleDateFormat("HH:mm", Locale.CHINA)
                .format(new Date(session.getStartTime().toEpochMilli()))
                + "-" + new SimpleDateFormat("HH:mm", Locale.CHINA)
                .format(new Date(session.getEndTime().toEpochMilli()));
        return "已对齐手表运动记录" + (title.length() > 0 ? "：" + title + " " : " ") + time;
    }

    /**
     * 只有采样够密、覆盖够全的读数才算这次训练真正的心率。
     *
     * <p>点完「结束」的那一刻，手表配套 App 往往还没把这次运动推进健康连接，库里只有
     * 每几分钟一次的后台抽样——那是静息心率。以前不做判定、读到就写死，而且写完之后
     * 重新同步的按钮就消失了，于是那个错误值永远留在记录里。
     */
    private void applyHeartRate(String key,
            List<android.health.connect.datatypes.HeartRateRecord> records,
            long startMs, long endMs, String watchSession, boolean silent) {
        List<HeartRateStats.Sample> samples = new ArrayList<HeartRateStats.Sample>();
        Set<String> origins = new LinkedHashSet<String>();
        for (android.health.connect.datatypes.HeartRateRecord record : records) {
            String origin = dataOriginLabel(record);
            for (android.health.connect.datatypes.HeartRateRecord.HeartRateSample sample : record.getSamples()) {
                long at = sample.getTime().toEpochMilli();
                if (at >= startMs && at <= endMs) {
                    samples.add(new HeartRateStats.Sample(at, (int) sample.getBeatsPerMinute()));
                    if (origin.length() > 0) {
                        origins.add(origin);
                    }
                }
            }
        }
        HeartRateStats stats = HeartRateStats.of(samples, startMs, endMs);
        int index = recordIndexByKey(key);
        if (index < 0) {
            return;
        }
        SessionRecord record = trainingRecords.get(index);

        if (stats.isEmpty()) {
            if (!silent) {
                Toast.makeText(this,
                        "这段时间还没有心率数据。手表配套 App 通常晚几分钟才同步到健康连接，稍后会自动重试。",
                        Toast.LENGTH_LONG).show();
            }
            return;
        }
        // 已经拿到过可靠数据就不让不可靠的读数把它覆盖掉。
        if (record.hrReliable && !stats.isReliable()) {
            if (!silent) {
                Toast.makeText(this, "这次读到的采样比已存的更稀疏，保留原来的心率。", Toast.LENGTH_LONG).show();
            }
            return;
        }

        String source = origins.isEmpty() ? "" : join(new ArrayList<String>(origins));
        if (watchSession.length() > 0) {
            source = source.length() > 0 ? watchSession + " · " + source : watchSession;
        }
        trainingRecords.set(index, record.withHeartRate(stats, seriesJson(samples, startMs), source));
        saveState();
        if ("records".equals(currentTab) && !inSession) {
            renderRecords();
        }
        if (!silent) {
            Toast.makeText(this, stats.isReliable()
                            ? "已同步：平均 " + stats.average() + " · 最高 " + stats.max()
                                    + "（" + stats.coverageLabel() + "）"
                            : "只读到 " + stats.coverageLabel() + "，可能是后台抽样而不是这次运动的心率，"
                                    + "手表同步完成后会自动重试。",
                    Toast.LENGTH_LONG).show();
        }
    }

    /** 训练结束后手表还没同步的记录，回到 App 时自动重试一次。 */
    private void retryPendingHeartRateSyncs() {
        if (!healthPermissionGranted() || trainingRecords.isEmpty()) {
            return;
        }
        long now = System.currentTimeMillis();
        int retried = 0;
        for (SessionRecord record : new ArrayList<SessionRecord>(trainingRecords)) {
            if (retried >= MAX_HR_RETRIES_PER_RESUME) {
                break;
            }
            if (record.epochMillis <= 0 || (record.hrReliable && (record.metrics.has("activeKcal") || record.metrics.has("totalKcal")))) {
                continue;
            }
            // 超过一天还没同步上就不再重试了，手表大概率根本没记这一段。
            if (now - record.epochMillis > HR_RETRY_WINDOW_MS) {
                continue;
            }
            retried++;
            syncHeartRateForRecord(recordKey(record), true);
        }
    }

    private String seriesJson(List<HeartRateStats.Sample> samples, long startMs) {
        samples = new ArrayList<>(samples);
        Collections.sort(samples, (a, b) -> Long.compare(a.timeMillis(), b.timeMillis()));
        JSONArray series = new JSONArray();
        int stride = Math.max(1, (int) Math.ceil(samples.size() / 360.0));
        for (int i = 0; i < samples.size(); i += stride) {
            JSONArray point = new JSONArray();
            point.put((samples.get(i).timeMillis() - startMs) / 1000);
            point.put(samples.get(i).bpm());
            series.put(point);
        }
        return series.toString();
    }

    /** 心率数据是哪个 App 写进健康连接的——对不上时一眼能看出是谁的问题。 */
    private String dataOriginLabel(android.health.connect.datatypes.Record record) {
        try {
            String pkg = record.getMetadata().getDataOrigin().getPackageName();
            if (pkg == null || pkg.length() == 0) {
                return "";
            }
            String friendly = KNOWN_HEALTH_APPS.get(pkg);
            if (friendly != null) {
                return friendly;
            }
            android.content.pm.PackageManager packages = getPackageManager();
            return packages.getApplicationLabel(
                    packages.getApplicationInfo(pkg, 0)).toString();
        } catch (Exception ignored) {
            return "";
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQ_HEALTH_PERMISSION) {
            boolean granted = healthPermissionGranted();
            String key = pendingHeartRateRecordKey;
            pendingHeartRateRecordKey = null;
            if (granted) {
                if (key != null) {
                    readHeartRate(key, false);
                } else {
                    Toast.makeText(this, "已授权，训练结束后会同步已授权的手表数据", Toast.LENGTH_LONG).show();
                    if ("settings".equals(currentTab)) {
                        renderSettings();
                    }
                }
            } else {
                Toast.makeText(this, "尚未授权运动数据，可在记录卡上重新授权", Toast.LENGTH_LONG).show();
            }
        }
    }

    private Exercise customExercise(String id, String name, List<String> regions, String instruction, String media) {
        return customExercise(id, name, regions, instruction, media,
                new ArrayList<String>(Arrays.asList("自重")));
    }

    private Exercise customExercise(String id, String name, List<String> regions, String instruction,
            String media, List<String> requiredEquipment) {
        List<String> safe = (regions == null || regions.isEmpty())
                ? new ArrayList<String>(Arrays.asList("背")) : regions;
        List<String> safeEquipment = (requiredEquipment == null || requiredEquipment.isEmpty())
                ? new ArrayList<String>(Arrays.asList("自重")) : requiredEquipment;
        List<String> steps = new ArrayList<String>();
        if (instruction != null) {
            for (String line : instruction.split("\\r?\\n")) {
                String trimmed = line.trim();
                if (trimmed.length() > 0) {
                    steps.add(trimmed);
                }
            }
        }
        if (steps.isEmpty()) {
            steps.add("用户自定义动作，待补充步骤。");
        }
        return new Exercise.Builder(id, name)
                .evidence(EvidenceStatus.USER_UNVERIFIED)
                .regions(safe.toArray(new String[0]))
                .patterns(patternForRegion(safe.get(0)))
                .equipment(safeEquipment.toArray(new String[0]))
                .stress("shoulder", StressLevel.MEDIUM)
                .stress("lower_back", StressLevel.LOW)
                .instructions(steps.toArray(new String[0]))
                .media(media)
                .build();
    }

    private String patternForRegion(String region) {
        if ("背".equals(region) || "手臂".equals(region)) {
            return "拉";
        }
        if ("胸".equals(region) || "肩".equals(region)) {
            return "推";
        }
        if ("腿".equals(region)) {
            return "蹲";
        }
        return "稳定";
    }

    private boolean matchesLibraryFilter(Exercise exercise) {
        if ("全部".equals(libraryFilter)) {
            return true;
        }
        if ("已标心".equals(libraryFilter)) {
            return favoriteIds.contains(exercise.id());
        }
        if ("我的动作".equals(libraryFilter)) {
            return isCustomExercise(exercise);
        }
        return exercise.targetRegions().contains(libraryFilter);
    }

    private void applyLibrarySearch(String raw) {
        libraryQuery = raw == null ? "" : raw.trim();
        libraryVisibleLimit = 60;
        renderLibrary(libraryFilter);
    }

    private boolean matchesLibraryQuery(Exercise exercise) {
        if (libraryQuery.length() == 0) {
            return true;
        }
        String query = libraryQuery.toLowerCase(Locale.ROOT);
        if (exercise.name().toLowerCase(Locale.ROOT).contains(query)) {
            return true;
        }
        return containsQuery(exercise.targetRegions(), query)
                || containsQuery(exercise.movementPatterns(), query)
                || containsQuery(exercise.equipment(), query)
                || containsQuery(exercise.requiredEquipment(), query)
                || containsQuery(exercise.primaryMuscles(), query)
                || containsQuery(exercise.secondaryMuscles(), query)
                || containsQuery(exercise.instructions(), query);
    }

    private boolean containsQuery(List<String> values, String query) {
        for (String value : values) {
            if (value != null && value.toLowerCase(Locale.ROOT).contains(query)) {
                return true;
            }
        }
        return false;
    }

    private void renderRecords() {
        currentTab = "records";
        clear();
        content.addView(title("记录", "训练用时与每个动作的完成情况"));
        if (currentPlan != null && !activeItems.isEmpty()) {
            LinearLayout current = card();
            current.addView(section((inSession ? "已暂存 · " : "待开始 · ") + currentPlan.title()));
            current.addView(text(inSession ? "已完成的组数与计时都已保留。" : "共 " + activeItems.size() + " 个动作，准备好即可开始。",
                    14, Typeface.NORMAL, MUTED));
            current.addView(space(10));
            current.addView(button(inSession ? "回到训练 →" : "开始这一练 →", GREEN, Color.WHITE, v -> startSession()),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));
            content.addView(current);
        }
        if (!trainingRecords.isEmpty()) {
            content.addView(statsCard());
        }
        content.addView(text("历史记录", 16, Typeface.BOLD, INK));
        if (trainingRecords.isEmpty()) {
            LinearLayout empty = card();
            empty.addView(text("还没有训练记录。生成一套组合、点“开始训练”，结束后会自动保存用时和每个动作。", 14, Typeface.NORMAL, MUTED));
            content.addView(empty);
        } else {
            for (int i = 0; i < trainingRecords.size(); i++) {
                content.addView(recordCard(i, trainingRecords.get(i)));
            }
        }
        renderBottomNav();
    }

    private View statsCard() {
        Calendar calendar = Calendar.getInstance();
        calendar.setFirstDayOfWeek(Calendar.MONDAY);
        calendar.set(Calendar.DAY_OF_WEEK, Calendar.MONDAY);
        calendar.set(Calendar.HOUR_OF_DAY, 0);
        calendar.set(Calendar.MINUTE, 0);
        calendar.set(Calendar.SECOND, 0);
        calendar.set(Calendar.MILLISECOND, 0);
        long weekStart = calendar.getTimeInMillis();

        int weekCount = 0;
        long weekSeconds = 0;
        for (SessionRecord record : trainingRecords) {
            if (record.epochMillis >= weekStart) {
                weekCount++;
                weekSeconds += durationSeconds(record.duration);
            }
        }
        LinearLayout card = card();
        card.addView(smallLabel("本周"));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(statCell(String.valueOf(weekCount), "次训练"));
        row.addView(statCell(formatDuration(weekSeconds), "总用时"));
        row.addView(statCell(String.valueOf(trainingRecords.size()), "累计次数"));
        card.addView(row);
        return card;
    }

    private View statCell(String value, String label) {
        LinearLayout cell = new LinearLayout(this);
        cell.setOrientation(LinearLayout.VERTICAL);
        cell.setGravity(Gravity.CENTER);
        cell.addView(text(value, 24, Typeface.BOLD, GREEN));
        cell.addView(text(label, 12, Typeface.NORMAL, MUTED));
        cell.setLayoutParams(new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        return cell;
    }

    private long durationSeconds(String duration) {
        int colon = duration == null ? -1 : duration.indexOf(':');
        if (colon <= 0) {
            return 0;
        }
        try {
            long minutes = Long.parseLong(duration.substring(0, colon));
            long seconds = Long.parseLong(duration.substring(colon + 1));
            return minutes * 60 + seconds;
        } catch (Exception ignored) {
            return 0;
        }
    }

    private View recordCard(final int index, SessionRecord record) {
        LinearLayout card = card();
        card.addView(text(record.title.length() == 0 ? record.time : record.time + " · " + record.title,
                15, Typeface.BOLD, INK));
        if (record.duration.length() > 0) {
            card.addView(text("训练用时：" + record.duration, 13, Typeface.BOLD, GREEN));
        }
        if (record.total > 0) {
            card.addView(text("完成 " + record.done + "/" + record.total + " 个动作", 13, Typeface.NORMAL, MUTED));
        }
        if (record.hrAvg > 0) {
            card.addView(text("心率：平均 " + record.hrAvg + " · 最高 " + record.hrMax
                    + " · 最低 " + record.hrMin + " bpm", 13, Typeface.BOLD, HEART_RED));
            // 来源和覆盖率摆出来，和手表对不上时能直接看出是哪一步的问题。
            StringBuilder hrMeta = new StringBuilder();
            if (record.hrSource.length() > 0) {
                hrMeta.append(record.hrSource).append(" · ");
            }
            hrMeta.append(record.hrSamples).append(" 个采样点 · 覆盖 ")
                    .append(record.hrCoveragePercent).append("%");
            card.addView(text(hrMeta.toString(), 12, Typeface.NORMAL, MUTED));
            if (!record.hrReliable) {
                card.addView(text("采样偏稀，可能是后台抽样而不是这次运动的心率；手表同步完成后重新同步会自动更新。",
                        12, Typeface.NORMAL, CORAL));
            }
        }
        if (!record.hrSeries.isEmpty()) card.addView(new HeartRateChart(this, record.hrSeries),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(160)));
        renderWatchMetrics(card, record);
        if (record.feel.length() > 0) {
            card.addView(text("强度感受：" + record.feel, 13, Typeface.NORMAL, MUTED));
        }
        if (record.pain.length() > 0) {
            card.addView(text("疼痛变化：" + record.pain, 13, Typeface.NORMAL,
                    "加重".equals(record.pain) ? CORAL : MUTED));
        }
        if (record.note.length() > 0) {
            card.addView(text("训练心得：" + record.note, 13, Typeface.NORMAL, INK));
        }
        if (!record.itemLines.isEmpty()) {
            card.addView(space(6));
            if (record.details.isEmpty()) for (String line : record.itemLines) card.addView(text(line, 13, Typeface.NORMAL, MUTED));
            else for (WorkoutEntry entry : record.details) card.addView(text(entry.line(), 13, Typeface.NORMAL, MUTED));
        }
        if (!record.timingNote.isEmpty()) card.addView(text(record.timingNote, 12, Typeface.NORMAL, MUTED));
        card.addView(button("写心得 / 备注", GREEN_SOFT, GREEN, v -> editRecordNote(recordKey(record))), fullButton());
        card.addView(button("修改动作、次数与重量", BG, GREEN, v -> editRecordItems(recordKey(record))), fullButton());
        card.addView(space(10));
        // 按钮永远留着：以前只在 hrAvg==0 时显示，第一次读到脏数据后就再也改不回来了。
        if (record.epochMillis > 0 && healthSupported()) {
            card.addView(button(record.hrAvg == 0 && record.metrics.length() == 0 ? "同步手表数据" : "重新同步手表数据", HEART_SOFT, HEART_RED,
                    v -> syncHeartRateForRecord(recordKey(record), false)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(40)));
            card.addView(space(8));
        }
        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        actions.addView(button("修改", Color.rgb(236, 240, 234), INK, v -> editRecord(index)),
                new LinearLayout.LayoutParams(0, dp(40), 1f));
        actions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        actions.addView(button("删除", Color.rgb(248, 235, 232), CORAL, v -> deleteRecord(index)),
                new LinearLayout.LayoutParams(0, dp(40), 1f));
        card.addView(actions);
        return card;
    }

    private void renderWatchMetrics(LinearLayout card, SessionRecord record) {
        JSONObject active = record.metrics.optJSONObject("activeKcal"), total = record.metrics.optJSONObject("totalKcal");
        if (active != null) card.addView(text("活动消耗：" + metricNumber(active, 0) + " 千卡", 19, Typeface.BOLD, GREEN));
        else if (total != null) card.addView(text("消耗热量：" + metricNumber(total, 0) + " 千卡（总热量）", 19, Typeface.BOLD, GREEN));
        else card.addView(text("消耗热量：暂无数据", 15, Typeface.BOLD, MUTED));
        if (total != null && active != null) card.addView(text("总热量：" + metricNumber(total, 0) + " 千卡（含静息消耗）", 13, Typeface.NORMAL, MUTED));
        else if (total != null) card.addView(text("总热量含静息消耗；活动热量暂无数据。", 12, Typeface.NORMAL, MUTED));
        JSONObject calories = active != null ? active : total;
        if (calories != null && calories.optInt("coverage", 100) < 100)
            card.addView(text("热量仅覆盖 " + calories.optInt("coverage") + "% 的训练时段，当前显示已记录部分。", 12, Typeface.NORMAL, AMBER));
        JSONObject steps = record.metrics.optJSONObject("steps"), distance = record.metrics.optJSONObject("distanceM");
        if (steps != null) card.addView(text("步数：" + metricNumber(steps, 0) + " 步", 13, Typeface.NORMAL, MUTED));
        if (distance != null) card.addView(text("距离：" + metricNumber(distance, 0) + " 米", 13, Typeface.NORMAL, MUTED));
        Set<String> origins = new LinkedHashSet<>();
        for (String key : new String[]{"activeKcal", "totalKcal", "steps", "distanceM"}) {
            JSONObject value = record.metrics.optJSONObject(key); if (value == null) continue;
            JSONArray sources = value.optJSONArray("sources"); if (sources == null) continue;
            for (int i = 0; i < sources.length(); i++) origins.add(KNOWN_HEALTH_APPS.getOrDefault(sources.optString(i), sources.optString(i)));
        }
        if (active != null || total != null || steps != null || distance != null)
            card.addView(text("健康连接 · " + (origins.isEmpty() ? "系统汇总" : join(new ArrayList<>(origins)))
                    + " · " + record.metrics.optString("windowLabel", "本次训练时间段"), 12, Typeface.NORMAL, MUTED));
    }

    private String metricNumber(JSONObject metric, int digits) {
        return String.format(Locale.CHINA, "%." + digits + "f", metric.optDouble("value", 0));
    }

    private void deleteRecord(int index) {
        if (index < 0 || index >= trainingRecords.size()) {
            return;
        }
        new AlertDialog.Builder(this)
                .setTitle("删除这条记录？")
                .setMessage("删除后无法恢复。")
                .setNegativeButton("取消", null)
                .setPositiveButton("删除", (dialog, which) -> {
                    if (index >= 0 && index < trainingRecords.size()) {
                        trainingRecords.remove(index);
                        saveState();
                        Toast.makeText(this, "已删除记录", Toast.LENGTH_SHORT).show();
                        renderRecords();
                    }
                })
                .show();
    }

    private SessionRecord recordCopy(SessionRecord old, String note, List<WorkoutEntry> entries) {
        List<String> lines = new ArrayList<>(), stats = new ArrayList<>(); int done = 0;
        for (WorkoutEntry e : entries) { lines.add(e.line()); if (!e.id.isEmpty()) stats.add(e.stat()); if (e.finished) done++; }
        SessionRecord result = new SessionRecord(old.time, old.title, entries.isEmpty() ? old.total : entries.size(),
                entries.isEmpty() ? old.done : done, old.feel, old.pain, note,
                entries.isEmpty() ? old.itemLines : lines, old.duration, old.epochMillis, old.startEpochMillis,
                old.hrAvg, old.hrMax, old.hrMin, old.hrSeries, old.hrSamples, old.hrCoveragePercent,
                old.hrReliable, old.hrSource, entries.isEmpty() ? old.itemStats : stats).copyExtras(old);
        result.details = new ArrayList<>(entries); return result;
    }

    private void editRecordNote(String key) {
        int index = recordIndexByKey(key); if (index < 0) return;
        EditText note = new EditText(this); note.setText(trainingRecords.get(index).note);
        note.setHint("今天的感受、动作要点、下次想调整什么……"); note.setContentDescription("训练心得 / 备注");
        note.setMinLines(4); note.setGravity(Gravity.TOP);
        note.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        new AlertDialog.Builder(this).setTitle("训练心得 / 备注").setView(note).setNegativeButton("取消", null)
                .setPositiveButton("保存心得", (d, w) -> {
                    int current = recordIndexByKey(key); if (current < 0) return;
                    SessionRecord old = trainingRecords.get(current);
                    trainingRecords.set(current, recordCopy(old, note.getText().toString().trim(), old.details));
                    saveState(); renderRecords();
                }).show();
    }

    private void editRecordItems(String key) {
        int index = recordIndexByKey(key); if (index < 0) return;
        SessionRecord record = trainingRecords.get(index);
        String[] names = new String[record.details.size()];
        for (int i = 0; i < names.length; i++) names[i] = (i + 1) + ". " + record.details.get(i).name;
        if (names.length == 0) { Toast.makeText(this, "这条旧记录没有保存动作明细", Toast.LENGTH_LONG).show(); return; }
        new AlertDialog.Builder(this).setTitle("选择要修改的动作").setItems(names, (d, which) -> {
            WorkoutEntry entry = record.details.get(which);
            WorkoutDoseEditor.show(this, entry.name, entry.dose, entry.restAfter, entry.weight, entry.completed, 1,
                    (dose, after, weight, completed) -> {
                        int current = recordIndexByKey(key); if (current < 0) return;
                        SessionRecord old = trainingRecords.get(current);
                        List<WorkoutEntry> entries = new ArrayList<>(old.details);
                        entries.set(which, new WorkoutEntry(entry.id, entry.name, dose, completed, completed == dose.sets(), after, weight, entry.original));
                        trainingRecords.set(current, recordCopy(old, old.note, entries)); saveState(); renderRecords();
                    });
        }).setNegativeButton("返回", null).show();
    }

    private void editRecord(int index) {
        if (index < 0 || index >= trainingRecords.size()) {
            return;
        }
        final SessionRecord record = trainingRecords.get(index);
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));

        box.addView(text("名称", 13, Typeface.BOLD, MUTED));
        final EditText title = new EditText(this);
        title.setText(record.title);
        title.setSingleLine(true);
        box.addView(title);

        box.addView(space(6));
        box.addView(text("整体强度感受", 13, Typeface.BOLD, MUTED));
        final String[] feels = {"轻松", "适中", "偏累", "很累"};
        final RadioGroup feelGroup = radioRow(feels, indexOf(feels, record.feel, 1), 5000);
        box.addView(wrapScroll(feelGroup));

        box.addView(space(6));
        box.addView(text("疼痛变化", 13, Typeface.BOLD, MUTED));
        final String[] pains = {"无", "减轻", "不变", "加重"};
        final RadioGroup painGroup = radioRow(pains, indexOf(pains, record.pain, 0), 6000);
        box.addView(wrapScroll(painGroup));

        final EditText note = new EditText(this);
        note.setText(record.note);
        note.setHint("训练心得 / 备注（可选）");
        note.setContentDescription("训练心得 / 备注");
        note.setMinLines(2);
        note.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        box.addView(note);

        ScrollView scroll = new ScrollView(this);
        scroll.addView(box);
        new AlertDialog.Builder(this)
                .setTitle("修改记录")
                .setView(scroll)
                .setNegativeButton("取消", null)
                .setPositiveButton("保存", (dialog, which) -> {
                    if (index < 0 || index >= trainingRecords.size()) {
                        return;
                    }
                    int current = recordIndexByKey(recordKey(record)); if (current < 0) return;
                    SessionRecord latest = trainingRecords.get(current);
                    SessionRecord updated = new SessionRecord(latest.time,
                            title.getText().toString().trim(),
                            latest.total, latest.done,
                            selectedLabel(feelGroup, feels, 5000),
                            selectedLabel(painGroup, pains, 6000),
                            note.getText().toString().trim(),
                            latest.itemLines, latest.duration, latest.epochMillis,
                            latest.startEpochMillis, latest.hrAvg, latest.hrMax, latest.hrMin,
                            latest.hrSeries, latest.hrSamples, latest.hrCoveragePercent,
                            latest.hrReliable, latest.hrSource, latest.itemStats).copyExtras(latest);
                    trainingRecords.set(current, updated);
                    saveState();
                    Toast.makeText(this, "已更新记录", Toast.LENGTH_SHORT).show();
                    renderRecords();
                })
                .show();
    }

    private int indexOf(String[] labels, String value, int fallback) {
        for (int i = 0; i < labels.length; i++) {
            if (labels[i].equals(value)) {
                return i;
            }
        }
        return fallback;
    }

    private void showSessionFeedback(final String key) {
        if (recordIndexByKey(key) < 0) {
            return;
        }
        final SessionRecord record = trainingRecords.get(recordIndexByKey(key));
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));
        box.addView(text("顺手记一下这次的感受，之后好调整强度。", 13, Typeface.NORMAL, MUTED));

        box.addView(space(8));
        box.addView(text("整体强度感受", 13, Typeface.BOLD, MUTED));
        final String[] feels = {"轻松", "适中", "偏累", "很累"};
        final RadioGroup feelGroup = radioRow(feels, indexOf(feels, record.feel, 1), 7000);
        box.addView(wrapScroll(feelGroup));

        box.addView(space(6));
        box.addView(text("疼痛变化", 13, Typeface.BOLD, MUTED));
        final String[] pains = {"无", "减轻", "不变", "加重"};
        final RadioGroup painGroup = radioRow(pains, indexOf(pains, record.pain, 0), 8000);
        box.addView(wrapScroll(painGroup));

        final EditText note = new EditText(this);
        note.setHint("训练心得 / 备注（可选）");
        note.setContentDescription("训练心得 / 备注");
        note.setMinLines(2);
        note.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        box.addView(note);

        ScrollView scroll = new ScrollView(this);
        scroll.addView(box);
        new AlertDialog.Builder(this)
                .setTitle("训练完成，感觉怎么样？")
                .setView(scroll)
                .setNegativeButton("稍后再填", null)
                .setPositiveButton("保存反馈", (dialog, which) -> {
                    int current = recordIndexByKey(key);
                    if (current < 0) {
                        return;
                    }
                    SessionRecord old = trainingRecords.get(current);
                    trainingRecords.set(current, new SessionRecord(old.time, old.title, old.total, old.done,
                            selectedLabel(feelGroup, feels, 7000),
                            selectedLabel(painGroup, pains, 8000),
                            note.getText().toString().trim(),
                            old.itemLines, old.duration, old.epochMillis,
                            old.startEpochMillis, old.hrAvg, old.hrMax, old.hrMin, old.hrSeries,
                            old.hrSamples, old.hrCoveragePercent, old.hrReliable, old.hrSource,
                            old.itemStats).copyExtras(old));
                    saveState();
                    Toast.makeText(this, "已保存训练反馈", Toast.LENGTH_SHORT).show();
                    if ("records".equals(currentTab) && !inSession) {
                        renderRecords();
                    }
                })
                .show();
    }

    private void renderSettings() {
        currentTab = "settings";
        clear();
        content.addView(title("设置", "强度、体能评估、器械和伤痛"));
        content.addView(appUpdateCard());
        content.addView(reviewScopeButton(this::renderSettings), fullButton());

        LinearLayout intensityCard = card();
        intensityCard.addView(section("默认强度与时长"));
        intensityCard.addView(intensityRow(true));
        intensityCard.addView(text("未手动选择时使用默认强度；本次手动选择优先。修改后重新生成训练生效。", 12, Typeface.NORMAL, MUTED));
        intensityCard.addView(space(6));
        intensityCard.addView(durationRow());
        content.addView(intensityCard);

        LinearLayout assessmentCard = card();
        assessmentCard.addView(section("体能评估"));
        assessmentCard.addView(space(4));
        if (assessment == null) {
            assessmentCard.addView(text("当前：未评估。日常训练不会被历史评估限强度；周期计划会先按初级水平起步。",
                    13, Typeface.NORMAL, MUTED));
            assessmentCard.addView(space(10));
            assessmentCard.addView(button("开始体能评估", GREEN, Color.WHITE,
                            v -> renderAssessmentForm(false, true)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        } else {
            String date = assessmentDate.length() == 0 ? "日期未记录" : assessmentDate;
            assessmentCard.addView(text("当前评估（" + date + "）：" + assessment.level().label()
                    + " · 强度上限 " + assessment.intensityCap().label(), 14, Typeface.BOLD,
                    assessment.medicalClearanceAdvised() ? CORAL : BLUE));
            assessmentCard.addView(space(4));
            assessmentCard.addView(text(assessment.medicalClearanceAdvised()
                            ? "安全筛查有「是」，日常训练会限制为低强度。可核对答案、重新评估或删除评估。"
                            : "可查看并修改已保存的答案，也可从空白问卷重新评估。",
                    13, Typeface.NORMAL, MUTED));
            assessmentCard.addView(space(10));
            LinearLayout assessmentActions = new LinearLayout(this);
            assessmentActions.setOrientation(LinearLayout.HORIZONTAL);
            assessmentActions.addView(button("查看 / 修改", GREEN, Color.WHITE,
                            v -> renderAssessmentForm(true, true)),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            assessmentActions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
            assessmentActions.addView(button("重新评估", BLUE, Color.WHITE,
                            v -> renderAssessmentForm(false, true)),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            assessmentCard.addView(assessmentActions);
            assessmentCard.addView(space(8));
            assessmentCard.addView(button("删除体能评估", Color.rgb(248, 235, 232), CORAL,
                            v -> confirmDeleteAssessment()),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        }
        content.addView(assessmentCard);

        LinearLayout equipmentCard = card();
        equipmentCard.addView(section("可用器械"));
        for (String item : equipmentOptions()) {
            CheckBox checkBox = new CheckBox(this);
            checkBox.setText(item);
            checkBox.setTextColor(INK);
            checkBox.setTextSize(15);
            checkBox.setChecked(equipment.contains(item));
            checkBox.setOnCheckedChangeListener((CompoundButton buttonView, boolean isChecked) -> {
                if (isChecked) {
                    equipment.add(item);
                } else {
                    equipment.remove(item);
                }
                saveState();
            });
            equipmentCard.addView(checkBox);
        }
        content.addView(equipmentCard);

        LinearLayout painCard = card();
        painCard.addView(section("伤痛部位"));
        painCard.addView(painRow("肩", shoulderPain, severity -> {
            shoulderPain = severity;
            saveState();
            renderSettings();
        }));
        painCard.addView(painRow("腰", lowerBackPain, severity -> {
            lowerBackPain = severity;
            saveState();
            renderSettings();
        }));
        painCard.addView(painRow("膝", kneePain, severity -> {
            kneePain = severity;
            saveState();
            renderSettings();
        }));
        content.addView(painCard);

        LinearLayout safety = card();
        safety.addView(section("安全边界"));
        safety.addView(text("这里用于帮助推荐避开可能刺激的动作，不用于诊断或治疗。急性损伤、麻木、放射痛、胸闷、头晕或疼痛持续加重时，请先咨询医生或物理治疗师。", 14, Typeface.NORMAL, MUTED));
        safety.addView(text("自动推荐仅使用已复核动作；动作库仍可查看全部动作。", 14, Typeface.BOLD, GREEN));
        content.addView(safety);

        content.addView(aiSettingsCard());

        LinearLayout backup = card();
        backup.addView(section("数据备份与迁移"));
        backup.addView(text("训练记录和菜谱库都只保存在本机。JSON 备份文件会同时包含两者，可以在任何设备上重新导入（包括以后的 iOS 版），文本导出适合发给自己阅读留底。", 14, Typeface.NORMAL, MUTED));
        backup.addView(space(10));
        backup.addView(button("备份到文件（JSON，可导入）", BLUE, Color.WHITE, v -> startBackupExport()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        backup.addView(space(8));
        backup.addView(button("从备份文件导入", GREEN, Color.WHITE, v -> startBackupImport()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        backup.addView(space(8));
        backup.addView(button("导出为文本（阅读用）", Color.rgb(236, 240, 234), INK, v -> exportRecords()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        content.addView(backup);

        LinearLayout watch = card();
        LinearLayout voice = card();
        voice.addView(section("训练语音口令"));
        voice.addView(space(6));
        final CheckBox voiceToggle = new CheckBox(this);
        voiceToggle.setText("开启语音口令（准备、开始、倒计时读秒、换边）");
        voiceToggle.setTextColor(INK);
        voiceToggle.setChecked(voiceEnabled);
        voiceToggle.setOnCheckedChangeListener((buttonView, checked) -> {
            voiceEnabled = checked;
            voiceCues.setEnabled(checked);
            saveState();
        });
        voice.addView(voiceToggle);
        voice.addView(space(4));
        voice.addView(text("用随包的中文语音片段播放，不依赖手机的 TTS 引擎，离线可用。"
                + "放着音乐时会短暂压低音乐音量而不是打断它。", 13, Typeface.NORMAL, MUTED));
        voice.addView(space(8));
        voice.addView(button("试听", Color.rgb(236, 240, 234), INK, v -> {
            voiceCues.setEnabled(true);
            voiceCues.begin();
            voiceCues.ready();
            content.postDelayed(() -> voiceCues.count(3), 700);
            content.postDelayed(() -> voiceCues.count(2), 1400);
            content.postDelayed(() -> voiceCues.count(1), 2100);
            content.postDelayed(voiceCues::go, 2800);
            content.postDelayed(voiceCues::end, 3800);
            if (!voiceEnabled) {
                content.postDelayed(() -> voiceCues.setEnabled(false), 4000);
            }
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        content.addView(voice);
        content.addView(space(10));

        watch.addView(section("手表运动数据"));
        if (Build.VERSION.SDK_INT >= 34) {
            watch.addView(text("从健康连接读取本次训练的心率、活动热量、总热量、步数和距离，只保存已授权且实际读到的数据。请先让手表配套 App 将数据同步到健康连接。", 14, Typeface.NORMAL, MUTED));
            watch.addView(space(10));
            if (healthPermissionGranted()) {
                watch.addView(noteBox("已授权部分或全部运动数据。训练结束后自动同步；旧记录可点“同步手表数据”。", GREEN));
            }
            if (!allHealthPermissionsGranted()) {
                watch.addView(button("授权心率、热量等运动数据", HEART_RED, Color.WHITE, v -> {
                    pendingHeartRateRecordKey = null;
                    requestPermissions(HEALTH_PERMISSIONS, REQ_HEALTH_PERMISSION);
                }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
            }
        } else {
            watch.addView(text("需要 Android 14 及以上（系统内置健康连接）。当前系统版本不支持，其余功能不受影响。", 14, Typeface.NORMAL, MUTED));
        }
        content.addView(watch);
        renderBottomNav();
        scrollToTop();
    }

    private View appUpdateCard() {
        LinearLayout card = card();
        card.addView(section("应用更新"));
        String version;
        try { version = getPackageManager().getPackageInfo(getPackageName(), 0).versionName; }
        catch (Exception ignored) { version = "未知"; }
        card.addView(text("当前版本 " + version + " · GitHub 私有项目", 13, Typeface.NORMAL, MUTED));
        githubUpdateStatusView = text(githubUpdateStatus, 13, Typeface.NORMAL, MUTED);
        card.addView(githubUpdateStatusView);
        card.addView(space(8));
        githubUpdateButton = button("检查更新", GREEN, Color.WHITE, v -> checkGitHubUpdate());
        githubUpdateButton.setEnabled(!githubUpdateBusy);
        card.addView(githubUpdateButton, fullButton());
        if (githubUpdateBusy) {
            card.addView(space(6));
            card.addView(button("取消", GREEN_SOFT, GREEN, v -> {
                githubUpdater.cancel();
                setGitHubUpdateStatus("更新操作已取消", false);
                renderSettings();
            }), fullButton());
        }
        if (pendingUpdateApk != null && pendingUpdateApk.isFile() && !githubUpdateBusy) {
            card.addView(space(6));
            card.addView(button("安装已下载更新", BLUE, Color.WHITE,
                    v -> launchUpdateInstaller(pendingUpdateApk)), fullButton());
        }
        String token = "";
        try { token = new GitHubTokenStore(this).read(); }
        catch (Exception ignored) { }
        card.addView(space(6));
        card.addView(text(token.isEmpty() ? "首次使用需配置私有项目的只读访问令牌。"
                : "已配置访问令牌，仅用于读取私有更新。", 12, Typeface.NORMAL, MUTED));
        Button configure = button("配置 GitHub 访问", GREEN_SOFT, GREEN, v -> configureGitHubAccess());
        configure.setEnabled(!githubUpdateBusy);
        card.addView(configure, fullButton());
        if (!token.isEmpty()) {
            Button clearToken = button("清除访问令牌", Color.rgb(236, 240, 234), INK, v -> {
                try {
                    new GitHubTokenStore(this).clear();
                    setGitHubUpdateStatus("访问令牌已清除", false);
                    renderSettings();
                } catch (Exception ignored) {
                    Toast.makeText(this, "未能清除访问令牌，请重试", Toast.LENGTH_LONG).show();
                }
            });
            clearToken.setEnabled(!githubUpdateBusy);
            card.addView(space(6));
            card.addView(clearToken, fullButton());
        }
        return card;
    }

    private void configureGitHubAccess() {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(20), dp(10), dp(20), dp(10));
        box.addView(text("使用 GitHub 的 Fine-grained token：只选择 TimeHouse 仓库，"
                + "Repository permissions → Contents 设为 Read-only。令牌会加密保存在本机。",
                14, Typeface.NORMAL, MUTED));
        final EditText tokenInput = new EditText(this);
        tokenInput.setSingleLine(true);
        tokenInput.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        tokenInput.setHint("粘贴只读访问令牌");
        tokenInput.setContentDescription("GitHub 只读访问令牌");
        box.addView(tokenInput);
        AlertDialog dialog = new AlertDialog.Builder(this).setTitle("配置私有更新")
                .setView(box).setNegativeButton("取消", null).setPositiveButton("保存", null)
                .setNeutralButton("创建只读令牌", (d, which) -> openExternal(
                        "https://github.com/settings/personal-access-tokens/new"
                        + "?name=TimeHouse-Updates&target_name=charlotteamian&expires_in=90&contents=read"))
                .create();
        dialog.setOnShowListener(d -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            String token = tokenInput.getText().toString().trim();
            if (!token.matches("(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}")) {
                tokenInput.setError("请填写有效的 GitHub 访问令牌");
                return;
            }
            try {
                new GitHubTokenStore(this).save(token);
                dialog.dismiss();
                setGitHubUpdateStatus("令牌已保存，可以检查更新", false);
                renderSettings();
            } catch (Exception ignored) {
                tokenInput.setError("令牌未能加密保存，请重试");
            }
        }));
        dialog.show();
    }

    private void setGitHubUpdateStatus(String status, boolean busy) {
        githubUpdateStatus = status;
        githubUpdateBusy = busy;
        if (githubUpdateStatusView != null) githubUpdateStatusView.setText(status);
        if (githubUpdateButton != null) githubUpdateButton.setEnabled(!busy);
    }

    private void checkGitHubUpdate() {
        if (githubUpdateBusy) return;
        if (inSession) {
            Toast.makeText(this, "请先结束本次训练，再更新应用", Toast.LENGTH_LONG).show();
            return;
        }
        final String token;
        final long installedCode;
        try {
            token = new GitHubTokenStore(this).read();
            installedCode = getPackageManager().getPackageInfo(getPackageName(), 0).getLongVersionCode();
        } catch (Exception ignored) {
            setGitHubUpdateStatus("请重新配置 GitHub 访问令牌", false);
            configureGitHubAccess();
            return;
        }
        if (token.isEmpty()) {
            configureGitHubAccess();
            return;
        }
        setGitHubUpdateStatus("正在检查 GitHub 新版本…", true);
        renderSettings();
        githubUpdater.check(token, new GitHubUpdater.CheckCallback() {
            @Override public void onRelease(GitHubUpdater.Release release) {
                if (isFinishing() || isDestroyed()) return;
                if (!GitHubUpdatePolicy.isNewer(release.versionCode, installedCode)) {
                    setGitHubUpdateStatus("当前已是最新版本；GitHub 版本 " + release.versionName, false);
                    if ("settings".equals(currentTab)) renderSettings();
                    return;
                }
                setGitHubUpdateStatus("发现新版本 " + release.versionName, false);
                if ("settings".equals(currentTab)) renderSettings();
                new AlertDialog.Builder(MainActivity.this).setTitle("更新到 " + release.versionName)
                        .setMessage("安装包约 " + (release.bytes / 1024 / 1024) + " MB。下载后会校验文件和签名，"
                                + "再打开系统安装界面。覆盖安装会保留现有记录。")
                        .setNegativeButton("稍后", null)
                        .setPositiveButton("下载并安装", (dialog, which) -> downloadGitHubUpdate(token, release)).show();
            }
            @Override public void onError(String message) {
                if (isFinishing() || isDestroyed()) return;
                setGitHubUpdateStatus(message, false);
                if ("settings".equals(currentTab)) renderSettings();
            }
        });
    }

    private void downloadGitHubUpdate(String token, GitHubUpdater.Release release) {
        pendingUpdateApk = null;
        setGitHubUpdateStatus("正在下载更新…", true);
        if ("settings".equals(currentTab)) renderSettings();
        githubUpdater.download(this, token, release, new GitHubUpdater.DownloadCallback() {
            @Override public void onProgress(long bytes, long total) {
                setGitHubUpdateStatus("正在下载 · " + (bytes * 100 / total) + "%（"
                        + (bytes / 1024 / 1024) + "/" + (total / 1024 / 1024) + " MB）", true);
            }
            @Override public void onReady(File apk) {
                if (isFinishing() || isDestroyed()) return;
                pendingUpdateApk = apk;
                setGitHubUpdateStatus("下载与签名校验通过，可以安装更新", false);
                if ("settings".equals(currentTab)) renderSettings();
                launchUpdateInstaller(apk);
            }
            @Override public void onError(String message) {
                if (isFinishing() || isDestroyed()) return;
                setGitHubUpdateStatus(message, false);
                if ("settings".equals(currentTab)) renderSettings();
            }
        });
    }

    private void launchUpdateInstaller(File apk) {
        if (inSession) {
            Toast.makeText(this, "请先结束本次训练，再安装更新", Toast.LENGTH_LONG).show();
            return;
        }
        if (apk == null || !apk.isFile()) {
            setGitHubUpdateStatus("安装包已被清理，请重新检查更新", false);
            return;
        }
        pendingUpdateApk = apk;
        if (!getPackageManager().canRequestPackageInstalls()) {
            new AlertDialog.Builder(this).setTitle("允许安装更新")
                    .setMessage("请在系统设置中允许“时光屋”安装应用。返回后会继续打开更新安装界面。")
                    .setNegativeButton("稍后", null)
                    .setPositiveButton("去授权", (dialog, which) -> {
                        try {
                            startActivityForResult(new Intent(android.provider.Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                                    Uri.parse("package:" + getPackageName())), REQ_UPDATE_INSTALL_PERMISSION);
                        } catch (Exception ignored) {
                            setGitHubUpdateStatus("无法打开安装权限设置，请在系统设置中手动允许", false);
                        }
                    }).show();
            return;
        }
        try {
            Uri uri = UpdateApkProvider.apkUri();
            Intent intent = new Intent(Intent.ACTION_VIEW).setDataAndType(uri, "application/vnd.android.package-archive");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            intent.setClipData(android.content.ClipData.newRawUri("时光屋更新", uri));
            startActivity(intent);
            setGitHubUpdateStatus("已打开系统安装界面", false);
        } catch (Exception ignored) {
            setGitHubUpdateStatus("无法打开安装界面，请稍后重试", false);
        }
    }

    private void confirmDeleteAssessment() {
        if (assessment == null) {
            return;
        }
        new AlertDialog.Builder(this)
                .setTitle("删除体能评估？")
                .setMessage("删除后将恢复为「未评估」，日常训练不再受这份评估的安全限强度影响。"
                        + "伤痛设置和训练记录不会被删除。")
                .setNegativeButton("取消", null)
                .setPositiveButton("确认删除", (dialog, which) -> {
                    assessment = null;
                    assessmentInput = null;
                    assessmentDate = "";
                    rebuildProgramAfterAssessmentChange();
                    invalidatePreparedWorkoutAfterAssessmentChange();
                    saveState();
                    Toast.makeText(this, "体能评估已删除，现为未评估状态", Toast.LENGTH_SHORT).show();
                    renderSettings();
                })
                .show();
    }

    /** 未开始的课程含旧评估日期和限强度原因，评估变更后必须重新生成。 */
    private void invalidatePreparedWorkoutAfterAssessmentChange() {
        if (inSession) {
            return;
        }
        currentPlan = null;
        activeItems.clear();
        pendingProgramKey = "";
    }

    /** 保留日历和完成记录，但立即用新评估重算后续周期的水平与强度上限。 */
    private void rebuildProgramAfterAssessmentChange() {
        if (program == null) {
            return;
        }
        TrainingLevel level = assessment == null ? TrainingLevel.BEGINNER : assessment.level();
        program = new ProgramBuilder().build(program.goal(), level, program.daysPerWeek(), assessmentCap());
    }

    private View aiSettingsCard() {
        LinearLayout card = card();
        card.addView(section("AI 推荐（可选）"));
        card.addView(text("开启后，「吃什么」会理解你当下的状态，支持库内挑选、联网菜谱、图片识别和链接解析；"
                        + "训练推荐仍先在本地做安全过滤，AI 只在安全动作里挑选。",
                14, Typeface.NORMAL, MUTED));
        card.addView(space(6));
        card.addView(noteBox("开启即代表：菜名、你输入的状态、训练目标和待识别图片会发送到 Google Gemini；"
                + "联网菜谱会发送到你选择的 Gemini 或 Groq。伤痛和心率等健康数据不会发送。关闭或未填对应 Key 时，"
                + "相关 AI 功能不可用，其余推荐使用本地逻辑。", AMBER));
        card.addView(space(10));

        final CheckBox enable = new CheckBox(this);
        enable.setText("启用 AI 推荐");
        enable.setTextColor(INK);
        enable.setTextSize(15);
        enable.setChecked(aiEnabled);
        card.addView(enable);

        card.addView(space(6));
        card.addView(text("Gemini API Key（在 Google AI Studio 免费获取）", 13, Typeface.BOLD, MUTED));
        final EditText key = new EditText(this);
        key.setHint("粘贴你的 API Key");
        key.setSingleLine(true);
        key.setText(aiApiKey);
        card.addView(key);

        card.addView(space(6));
        card.addView(text("普通 AI 模型（训练、库内推荐和图片识别）", 13, Typeface.BOLD, MUTED));
        final EditText model = new EditText(this);
        model.setHint(GeminiModelName.DEFAULT_MODEL);
        model.setSingleLine(true);
        model.setText(aiModel);
        card.addView(model);

        card.addView(space(12));
        card.addView(section("联网搜索服务"));
        final RadioGroup searchProvider = new RadioGroup(this);
        searchProvider.setOrientation(RadioGroup.HORIZONTAL);
        final RadioButton providerGroq = new RadioButton(this);
        providerGroq.setText("Groq（免费）");
        providerGroq.setTextColor(INK);
        final RadioButton providerGemini = new RadioButton(this);
        providerGemini.setText("Gemini");
        providerGemini.setTextColor(INK);
        providerGroq.setId(View.generateViewId());
        providerGemini.setId(View.generateViewId());
        searchProvider.addView(providerGroq, new RadioGroup.LayoutParams(0, dp(44), 1f));
        searchProvider.addView(providerGemini, new RadioGroup.LayoutParams(0, dp(44), 1f));
        searchProvider.check(isGroqSearchProvider() ? providerGroq.getId() : providerGemini.getId());
        card.addView(searchProvider);

        card.addView(text("联网搜索 API Key", 13, Typeface.BOLD, MUTED));
        card.addView(text("Groq 使用 gsk_ 开头的免费 Key；Gemini 可留空并复用上面的 Key。",
                12, Typeface.NORMAL, MUTED));
        final EditText searchKey = new EditText(this);
        searchKey.setHint(isGroqSearchProvider() ? "粘贴 Groq API Key" : "留空 = 使用上面的 Gemini Key");
        searchKey.setSingleLine(true);
        searchKey.setText(aiSearchApiKey);
        card.addView(searchKey);

        card.addView(space(6));
        card.addView(text("联网搜索 API 地址", 13, Typeface.BOLD, MUTED));
        final EditText searchEndpoint = new EditText(this);
        searchEndpoint.setHint(GroqEndpoint.DEFAULT_ENDPOINT);
        searchEndpoint.setSingleLine(true);
        searchEndpoint.setText(aiSearchEndpoint);
        searchEndpoint.setEnabled(isGroqSearchProvider());
        card.addView(searchEndpoint);

        card.addView(space(6));
        card.addView(text("联网搜索模型", 13, Typeface.BOLD, MUTED));
        final EditText searchModel = new EditText(this);
        searchModel.setHint(isGroqSearchProvider() ? GroqEndpoint.DEFAULT_MODEL : GeminiModelName.DEFAULT_MODEL);
        searchModel.setSingleLine(true);
        searchModel.setText(aiSearchModel);
        card.addView(searchModel);

        providerGroq.setOnClickListener(v -> {
            searchEndpoint.setEnabled(true);
            searchEndpoint.setHint(GroqEndpoint.DEFAULT_ENDPOINT);
            searchKey.setHint("粘贴 Groq API Key");
            String current = searchModel.getText().toString().trim();
            if (current.length() == 0 || current.startsWith("gemini-")) {
                searchModel.setText(GroqEndpoint.DEFAULT_MODEL);
            }
            if (searchEndpoint.getText().toString().trim().length() == 0) {
                searchEndpoint.setText(GroqEndpoint.DEFAULT_ENDPOINT);
            }
        });
        providerGemini.setOnClickListener(v -> {
            searchEndpoint.setEnabled(false);
            searchKey.setHint("留空 = 使用上面的 Gemini Key");
            String current = searchModel.getText().toString().trim();
            if (current.length() == 0 || current.startsWith("groq/")) {
                searchModel.setText(GeminiModelName.DEFAULT_MODEL);
            }
        });

        card.addView(space(10));
        card.addView(button("保存 AI 设置", GREEN, Color.WHITE, v -> {
            aiEnabled = enable.isChecked();
            aiApiKey = key.getText().toString().trim();
            aiModel = GeminiModelName.normalize(model.getText().toString());
            aiSearchProvider = searchProvider.getCheckedRadioButtonId() == providerGroq.getId()
                    ? SEARCH_PROVIDER_GROQ : SEARCH_PROVIDER_GEMINI;
            aiSearchApiKey = searchKey.getText().toString().trim();
            if (isGroqSearchProvider()) {
                aiSearchEndpoint = GroqEndpoint.normalize(searchEndpoint.getText().toString());
                aiSearchModel = searchModel.getText().toString().trim();
                if (aiSearchModel.length() == 0) {
                    aiSearchModel = GroqEndpoint.DEFAULT_MODEL;
                }
            } else {
                aiSearchEndpoint = "";
                aiSearchModel = GeminiModelName.normalize(searchModel.getText().toString());
            }
            saveState();
            if (aiEnabled && aiApiKey.length() == 0) {
                Toast.makeText(this, "已开启，但还没填 Key，暂时仍用本地推荐", Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(this, aiEnabled ? "已开启 AI 推荐" : "已保存（AI 关闭，使用本地推荐）",
                        Toast.LENGTH_SHORT).show();
            }
            renderSettings();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        card.addView(space(8));
        card.addView(button("如何获取免费 Key（打开 AI Studio）", Color.rgb(236, 240, 234), INK,
                v -> openExternal("https://aistudio.google.com/app/apikey")),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        card.addView(space(8));
        card.addView(button("获取 Groq 免费 Key", Color.rgb(236, 240, 234), INK,
                v -> openExternal("https://console.groq.com/keys")),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        return card;
    }

    private void exportRecords() {
        if (trainingRecords.isEmpty() && recipes.isEmpty()) {
            Toast.makeText(this, "还没有训练记录或菜谱可以导出", Toast.LENGTH_SHORT).show();
            return;
        }
        StringBuilder builder = new StringBuilder("健身训练记录（共 " + trainingRecords.size() + " 次）\n");
        for (SessionRecord record : trainingRecords) {
            builder.append("\n").append(record.time);
            if (record.title.length() > 0) {
                builder.append(" · ").append(record.title);
            }
            if (record.duration.length() > 0) {
                builder.append(" · 用时 ").append(record.duration);
            }
            if (record.total > 0) {
                builder.append(" · 完成 ").append(record.done).append("/").append(record.total);
            }
            builder.append("\n");
            if (record.hrAvg > 0) {
                builder.append("心率：平均 ").append(record.hrAvg)
                        .append(" · 最高 ").append(record.hrMax)
                        .append(" · 最低 ").append(record.hrMin).append(" bpm\n");
            }
            if (record.feel.length() > 0) {
                builder.append("强度感受：").append(record.feel).append("\n");
            }
            if (record.pain.length() > 0) {
                builder.append("疼痛变化：").append(record.pain).append("\n");
            }
            if (record.note.length() > 0) {
                builder.append("备注：").append(record.note).append("\n");
            }
            if (record.details.isEmpty()) for (String line : record.itemLines) builder.append("  ").append(line).append("\n");
            else for (WorkoutEntry entry : record.details) builder.append("  ").append(entry.line()).append("\n");
            for (String key : new String[]{"activeKcal", "totalKcal", "steps", "distanceM"}) {
                JSONObject value = record.metrics.optJSONObject(key);
                if (value != null) builder.append(key.equals("activeKcal") ? "活动热量（千卡）" : key.equals("totalKcal") ? "总热量（千卡）" : key.equals("steps") ? "步数" : "距离（米）")
                        .append(": ").append(metricNumber(value, 0)).append("\n");
            }
        }
        if (!recipes.isEmpty()) {
            builder.append("\n————————\n菜谱库（共 ").append(recipes.size()).append(" 个）\n");
            for (Recipe recipe : recipes) {
                builder.append("\n").append(recipe.name);
                if (recipe.rating > 0) {
                    builder.append(" · ").append(stars(recipe.rating));
                }
                builder.append("\n");
                if (!recipe.tags.isEmpty()) {
                    builder.append("口味：").append(join(recipe.tags)).append("\n");
                }
                if (!recipe.ingredients.isEmpty()) {
                    builder.append("配料：").append(join(recipe.ingredients)).append("\n");
                }
                if (!recipe.steps.isEmpty()) {
                    builder.append("做法：\n");
                    for (int s = 0; s < recipe.steps.size(); s++) {
                        builder.append("  ").append(s + 1).append(". ")
                                .append(recipe.steps.get(s).text).append("\n");
                    }
                }
                if (recipe.review.length() > 0) {
                    builder.append("点评：").append(recipe.review).append("\n");
                }
                if (recipe.note.length() > 0) {
                    builder.append("记录：").append(recipe.note).append("\n");
                }
            }
        }
        Intent send = new Intent(Intent.ACTION_SEND);
        send.setType("text/plain");
        send.putExtra(Intent.EXTRA_SUBJECT, "健身训练记录与菜谱");
        send.putExtra(Intent.EXTRA_TEXT, builder.toString());
        try {
            startActivity(Intent.createChooser(send, "导出训练记录"));
        } catch (Exception ignored) {
            Toast.makeText(this, "没有可用的分享应用", Toast.LENGTH_SHORT).show();
        }
    }

    private void renderFood() {
        currentTab = "food";
        clear();
        content.addView(title("吃什么", "先看今天缺什么，再决定吃什么"));

        content.addView(nutritionSummaryCard());
        content.addView(space(10));
        if (nutritionProfile != null && energyPlan != null) {
            content.addView(todayFoodLogCard());
            content.addView(space(10));
        }

        LinearLayout ask = card();
        ask.addView(section("今天吃什么"));
        ask.addView(space(4));
        if (energyPlan != null && pagodaTargets != null) {
            ask.addView(text(todayGap().summary(), 13, Typeface.BOLD, AMBER));
            ask.addView(space(4));
            ask.addView(text("推荐会按今日缺口、剩余热量和你现在的状态来挑。",
                    12, Typeface.NORMAL, MUTED));
            ask.addView(space(8));
            ask.addView(mealSlotChips());
            ask.addView(space(8));
        } else {
            ask.addView(text("先填营养档案，推荐才能按热量和宝塔缺口来挑，否则只能按口味。",
                    12, Typeface.NORMAL, MUTED));
            ask.addView(space(8));
        }
        foodPreferenceInput = new EditText(this);
        foodPreferenceInput.setSingleLine(false);
        foodPreferenceInput.setMinLines(1);
        foodPreferenceInput.setHint("说说现在的状态，比如：很累不想久做 / 心情低落 / 刚运动完 / 想吃辣的");
        foodPreferenceInput.setTextColor(INK);
        foodPreferenceInput.setHintTextColor(Color.rgb(126, 137, 132));
        foodPreferenceInput.setTextSize(15);
        foodPreferenceInput.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        foodPreferenceInput.setBackground(bg(Color.rgb(249, 251, 247), dp(8), LINE, 1));
        foodPreferenceInput.setPadding(dp(12), dp(10), dp(12), dp(10));
        foodPreferenceInput.setText(foodPreferenceText);
        ask.addView(foodPreferenceInput, matchWrap());
        ask.addView(space(10));
        LinearLayout askActions = new LinearLayout(this);
        askActions.setOrientation(LinearLayout.HORIZONTAL);
        askActions.addView(button("从菜谱库挑", GREEN, Color.WHITE, v -> recommendFood(false)),
                new LinearLayout.LayoutParams(0, dp(46), 1f));
        askActions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        askActions.addView(button("联网找菜", BLUE, Color.WHITE, v -> recommendFood(true)),
                new LinearLayout.LayoutParams(0, dp(46), 1f));
        ask.addView(askActions);
        ask.addView(space(6));
        ask.addView(text("联网只搜 " + RecipeSources.recipePromptList() + "，其他来源不采用。",
                11, Typeface.NORMAL, MUTED));
        content.addView(ask);

        if (aiThinking) {
            content.addView(aiThinkingCard(lastRecommendRandom
                    ? "AI 正在按今天的缺口，去下厨房等菜谱站找一道…"
                    : "AI 正在结合今天的缺口和你的状态，从菜谱库里帮你挑…"));
        } else {
            BuiltinRecipe science = builtinRecipeById(scienceRecId);
            Recipe recommended = recommendedWebRecipe != null
                    ? recommendedWebRecipe : recipeById(recommendedRecipeId);
            if (recommended != null) {
                content.addView(recommendedCard(recommended));
            } else if (science != null) {
                LinearLayout pick = card();
                pick.addView(smallLabel("按今日缺口推荐"));
                pick.addView(space(6));
                pick.addView(builtinRecipeRow(science, scienceRecReason));
                content.addView(pick);
            }
        }

        LinearLayout tools = new LinearLayout(this);
        tools.setOrientation(LinearLayout.HORIZONTAL);
        Button toolManual = button("手动录入", GREEN, Color.WHITE, v -> openRecipeEditor(null));
        Button toolImage = button("图片识别", BLUE, Color.WHITE, v -> pickRecipeImport());
        Button toolLink = button("链接解析", Color.rgb(120, 110, 150), Color.WHITE, v -> askRecipeLink());
        for (Button tool : new Button[]{toolManual, toolImage, toolLink}) {
            tool.setSingleLine(true);
            tool.setTextSize(13);
            tool.setPadding(dp(4), 0, dp(4), 0);
        }
        tools.addView(toolManual, new LinearLayout.LayoutParams(0, dp(44), 1f));
        tools.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
        tools.addView(toolImage, new LinearLayout.LayoutParams(0, dp(44), 1f));
        tools.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
        tools.addView(toolLink, new LinearLayout.LayoutParams(0, dp(44), 1f));
        content.addView(tools);
        content.addView(space(4));
        content.addView(text("图片识别 / 链接解析需要在设置里开启 AI 并填入 Key。", 12, Typeface.NORMAL, MUTED));
        content.addView(space(6));

        renderRecipeLibrary();
        renderBottomNav();
    }

    /**
     * 菜谱库：我自己的菜谱和循证食谱在同一个列表里，不再分两处。
     * 循证的带「循证」标记，收进我的菜谱后就以副本身份出现，不会重复显示两条。
     */
    private void renderRecipeLibrary() {
        List<BuiltinRecipe> unsaved = new ArrayList<BuiltinRecipe>();
        for (BuiltinRecipe builtin : builtinRecipes) {
            if (savedCopyOfBuiltin(builtin.id()) == null) {
                unsaved.add(builtin);
            }
        }
        content.addView(text("菜谱库（" + (recipes.size() + unsaved.size()) + "）",
                16, Typeface.BOLD, INK));
        content.addView(space(6));
        content.addView(chips(new String[]{"all", "mine", "science"},
                new String[]{"全部", "我的（" + recipes.size() + "）", "循证（" + unsaved.size() + "）"},
                recipeFilter, value -> {
                    recipeFilter = value;
                    renderFood();
                }));
        content.addView(space(6));
        int shown = 0;
        if (!"science".equals(recipeFilter)) {
            for (Recipe recipe : recipes) {
                content.addView(recipeCard(recipe));
                shown++;
            }
        }
        if (!"mine".equals(recipeFilter)) {
            for (BuiltinRecipe builtin : unsaved) {
                content.addView(builtinLibraryCard(builtin));
                shown++;
            }
        }
        if (shown == 0) {
            LinearLayout empty = card();
            empty.addView(text("这里还是空的。把做成功的菜记进来：可以手动录入，也可以用「图片识别」"
                    + "把一张菜谱截图自动拆成配料和步骤；循证食谱点「收进我的菜谱」也会出现在这里。",
                    14, Typeface.NORMAL, MUTED));
            content.addView(empty);
        }
    }

    private View mealSlotChips() {
        return chips(new String[]{"", "早餐", "午餐", "晚餐", "加餐"},
                new String[]{"自动", "早餐", "午餐", "晚餐", "加餐"},
                scienceSlot, value -> {
                    scienceSlot = value;
                    renderFood();
                });
    }

    private View chips(String[] values, String[] labels, String selected, ChipPick pick) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        for (int i = 0; i < values.length; i++) {
            final String value = values[i];
            boolean on = value.equals(selected == null ? "" : selected);
            TextView chip = text(labels[i], 13, on ? Typeface.BOLD : Typeface.NORMAL,
                    on ? Color.WHITE : INK);
            chip.setPadding(dp(12), dp(6), dp(12), dp(6));
            chip.setBackground(bg(on ? GREEN : Color.rgb(240, 243, 238), dp(15), on ? GREEN : LINE, 1));
            chip.setOnClickListener(v -> pick.pick(value));
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            lp.setMargins(0, 0, dp(8), 0);
            row.addView(chip, lp);
        }
        return wrapScroll(row);
    }

    /** 循证食谱在菜谱库列表里的样子：和我的菜谱同一种卡片，只多一个「循证」标记。 */
    private View builtinLibraryCard(final BuiltinRecipe builtin) {
        LinearLayout card = card();
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.addView(recipeImage("", 76), new LinearLayout.LayoutParams(dp(76), dp(76)));
        row.addView(space(12), new LinearLayout.LayoutParams(dp(12), 1));
        LinearLayout texts = new LinearLayout(this);
        texts.setOrientation(LinearLayout.VERTICAL);
        texts.addView(text(builtin.name(), 16, Typeface.BOLD, INK));
        texts.addView(text("循证 · " + join(builtin.mealSlots()), 12, Typeface.BOLD, GREEN));
        texts.addView(text(builtin.macroLabel(), 12, Typeface.NORMAL, MUTED));
        row.addView(texts, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        card.addView(row);
        card.setOnClickListener(v -> renderBuiltinRecipeDetail(builtin));
        return card;
    }

    private void recommendFood(boolean randomMode) {
        if (foodPreferenceInput != null) {
            foodPreferenceText = foodPreferenceInput.getText().toString().trim();
        }
        lastRecommendRandom = randomMode;
        if (randomMode) {
            if (!webSearchConfigured()) {
                promptEnableAi("联网找菜");
                return;
            }
            recommendFoodFromWeb();
            return;
        }
        if (recipes.isEmpty() && builtinRecipes.isEmpty()) {
            Toast.makeText(this, "菜谱库还是空的，可以点「联网找菜」去下厨房找一道", Toast.LENGTH_SHORT).show();
            return;
        }
        if (aiConfigured()) {
            recommendFoodWithAi();
            return;
        }
        localFoodPick();
    }

    /**
     * 不联网、不用 AI 的推荐：仍然从今日缺口出发，用 {@link RecipeScorer} 在
     * 循证食谱 + 我的菜谱（有营养估算的）里排序，而不是随机抽一道。
     * 没填营养档案时才退回到按口味匹配。
     */
    private void localFoodPick() {
        aiThinking = false;
        if (energyPlan != null && pagodaTargets != null) {
            String slot = scienceSlot.length() == 0 ? currentMealSlot() : scienceSlot;
            List<RecipeScorer.Scored> ranked = rankLibrary(slot);
            if (ranked.isEmpty()) {
                ranked = rankLibrary("");   // 这个时段没有合适的就不限时段
            }
            if (!ranked.isEmpty()) {
                applyRankedPick(pickFromRanked(ranked));
                if ("food".equals(currentTab)) {
                    renderFood();
                }
                return;
            }
        }
        Recipe picked = pickRecipe(foodPreferenceText, recommendedRecipeId);
        if (picked != null) {
            clearRecommendation();
            recommendedRecipeId = picked.id;
        }
        if ("food".equals(currentTab)) {
            renderFood();
        }
    }

    /**
     * 在按缺口排好的候选里落定一道：口味优先在前几名里找，找不到就用第一名；
     * 和上次推的是同一道时顺延一位，免得「换一个」原地不动。
     */
    private RecipeScorer.Scored pickFromRanked(List<RecipeScorer.Scored> ranked) {
        RecipeScorer.Scored chosen = null;
        if (foodPreferenceText.length() > 0) {
            for (RecipeScorer.Scored scored : ranked) {
                if (matchScore(scored.recipe, foodPreferenceText) > 0
                        && !isLastRecommended(scored.recipe.id())) {
                    chosen = scored;
                    break;
                }
            }
        }
        if (chosen == null) {
            for (RecipeScorer.Scored scored : ranked) {
                if (!isLastRecommended(scored.recipe.id())) {
                    chosen = scored;
                    break;
                }
            }
        }
        return chosen == null ? ranked.get(0) : chosen;
    }

    private boolean isLastRecommended(String id) {
        return id.equals(scienceRecId) || id.equals(recommendedRecipeId);
    }

    /** 排序结果里的 id 可能是循证食谱，也可能是我自己的菜谱，分别落到对应的展示位。 */
    private void applyRankedPick(RecipeScorer.Scored top) {
        Recipe mine = recipeById(top.recipe.id());
        clearRecommendation();
        if (mine != null) {
            recommendedRecipeId = mine.id;
            recommendedRecipeReason = top.reason;
        } else {
            scienceRecId = top.recipe.id();
            scienceRecReason = "推荐理由：" + top.reason;
        }
    }

    private void clearRecommendation() {
        recommendedRecipeId = null;
        recommendedWebRecipe = null;
        recommendedRecipeReason = "";
        scienceRecId = "";
        scienceRecReason = "";
    }

    private void recommendFoodWithAi() {
        aiThinking = true;
        renderFood();
        final String slot = scienceSlot.length() == 0 ? currentMealSlot() : scienceSlot;
        String prompt = buildFoodPrompt(foodPreferenceText, slot);
        geminiClient.generate(aiApiKey, aiModel, prompt, new GeminiClient.Callback() {
            @Override
            public void onResult(String text) {
                aiThinking = false;
                if (!applyFoodAiPick(text)) {
                    Toast.makeText(MainActivity.this, "AI 结果不可用，已按今日缺口推荐",
                            Toast.LENGTH_SHORT).show();
                    localFoodPick();
                    return;
                }
                if ("food".equals(currentTab)) {
                    renderFood();
                }
            }

            @Override
            public void onError(String message) {
                aiThinking = false;
                Toast.makeText(MainActivity.this, "AI 暂时不可用（" + message + "），已按今日缺口推荐",
                        Toast.LENGTH_LONG).show();
                localFoodPick();
            }
        });
    }

    private void recommendFoodFromWeb() {
        final String previousWebName = recommendedWebRecipe == null ? "" : recommendedWebRecipe.name;
        aiThinking = true;
        recommendedWebRecipe = null;
        renderFood();
        StringBuilder prompt = new StringBuilder();
        prompt.append("你是用户的私人营养顾问兼做饭助手。请使用联网搜索工具找一道真实可做的菜谱。\n")
                .append("只允许采用这些网站上的菜谱：").append(RecipeSources.recipePromptList())
                .append("。搜索时请带上站点名或用 site: 限定，")
                .append("source_url 必须是这些站点上的具体菜谱页面，不是首页、搜索结果页或其他网站。")
                .append("找不到就明说找不到，不要用别的站凑数，更不要编造链接。\n");
        if (energyPlan != null && pagodaTargets != null) {
            prompt.append("今日营养情况：").append(todayGap().promptBrief()).append("\n")
                    .append("这一餐是：")
                    .append(scienceSlot.length() == 0 ? currentMealSlot() : scienceSlot).append("。\n")
                    .append("先按这个缺口和剩余热量筛，再在符合的菜里挑贴合用户状态的一道。\n");
            prompt.append("热量和营养估算可参考 ").append(RecipeSources.nutritionPromptList())
                    .append("，估不准就按常见食物成分给保守值。\n");
        }
        prompt.append("用户当前状态：")
                .append(foodPreferenceText.length() == 0 ? "没有特殊要求" : foodPreferenceText).append("\n");
        if (recommendedRecipeId != null) {
            Recipe previous = recipeById(recommendedRecipeId);
            if (previous != null) {
                prompt.append("这次不要推荐「").append(previous.name).append("」。\n");
            }
        } else if (previousWebName.length() > 0) {
            prompt.append("这次不要再推荐「").append(previousWebName).append("」，请换一道。\n");
        }
        prompt.append("只返回一个 JSON 对象，不要 Markdown：")
                .append("{\"name\":\"菜名\",\"reason\":\"一句话说明为什么适合：要点出补了哪个缺口或热量为什么合适\",")
                .append("\"source_url\":\"你实际参考的菜谱网页完整 https 链接\",\"image_url\":\"可选的菜品图片 https 链接\",")
                .append("\"tags\":[\"快手\",\"清淡\"],\"ingredients\":[\"配料名 用量\"],\"steps\":[\"第一步\",\"第二步\"],")
                .append("\"kcal\":单人份热量整数,\"protein_g\":蛋白克数整数,\"fiber_g\":纤维克数整数,")
                .append("\"pagoda_grams\":{类别:生重克数}}。")
                .append("pagoda_grams 的类别只能用这些键：").append(pagodaKeyList()).append("；")
                .append("一律填生重/干重（一碗熟米饭记 GRAIN 80，不是熟重 200），没有的类别就不要写。")
                .append("配料和步骤必须来自搜索到的菜谱，保留用量、火候和时间等关键信息，不要编造来源链接。");

        generateWithWebProvider(prompt.toString(), new GeminiClient.Callback() {
            @Override
            public void onModelFallback(String requestedModel, String fallbackModel) {
                persistWebSearchModelFallback(requestedModel, fallbackModel);
            }

            @Override
            public void onResult(String text) {
                aiThinking = false;
                Recipe recipe = parseWebRecipe(text);
                if (recipe == null) {
                    Toast.makeText(MainActivity.this,
                            "没拿到可用结果：只采用 " + RecipeSources.recipePromptList()
                                    + " 上的菜谱，换个说法再试一次", Toast.LENGTH_LONG).show();
                } else {
                    String reason = recommendedRecipeReason;
                    clearRecommendation();
                    recommendedWebRecipe = recipe;
                    recommendedRecipeReason = reason;
                }
                if ("food".equals(currentTab)) {
                    renderFood();
                }
            }

            @Override
            public void onError(String message) {
                aiThinking = false;
                Toast.makeText(MainActivity.this, "联网搜索失败：" + message, Toast.LENGTH_LONG).show();
                if ("food".equals(currentTab)) {
                    renderFood();
                }
            }
        });
    }

    private Recipe parseWebRecipe(String text) {
        try {
            JSONObject object = new JSONObject(text);
            Recipe recipe = recipeFromAiObject(object);
            String sourceUrl = object.optString("source_url", "").trim();
            if (recipe == null || !isWebUrl(sourceUrl)) {
                return null;
            }
            // 白名单之外的链接一律不认：提示词只是请求，这里才是真正的门
            if (!RecipeSources.isRecipeSource(sourceUrl)) {
                return null;
            }
            recipe.id = "web_recipe_" + System.currentTimeMillis();
            recipe.sourceUrl = sourceUrl;
            String imageUrl = object.optString("image_url", "").trim();
            if (isWebUrl(imageUrl)) {
                recipe.sourceMedia = imageUrl;
            }
            recommendedRecipeReason = object.optString("reason", "").trim();
            return recipe;
        } catch (Exception ignored) {
            return null;
        }
    }

    /**
     * 库内推荐的提示词：先给今日缺口，再给候选（我的菜谱 + 循证食谱），
     * 让 AI 在营养约束下按口味选，而不是只按口味选。
     */
    private String buildFoodPrompt(String pref, String slot) {
        StringBuilder builder = new StringBuilder();
        builder.append("你是用户的私人营养顾问兼做饭助手。用户不知道今天吃什么，请从下面的候选里挑一道。\n");
        if (energyPlan != null && pagodaTargets != null) {
            builder.append("今日营养情况：").append(todayGap().promptBrief()).append("\n");
            builder.append("这一餐是：").append(slot).append("。\n");
        }
        builder.append("用户当前状态（口味、时间、身体感受、心情）：")
                .append(pref.length() == 0 ? "没有特殊要求" : pref).append("\n");
        builder.append("选择原则：先满足营养缺口和剩余热量，再在满足的前提下贴合用户状态；")
                .append("两者冲突时说明取舍理由。\n");
        if (scienceRecId.length() > 0 || recommendedRecipeId != null) {
            builder.append("不要再选 id 为 ").append(scienceRecId.length() > 0 ? scienceRecId : recommendedRecipeId)
                    .append(" 的那道，换一道。\n");
        }
        builder.append("候选（id | 名称 | 说明）：\n");
        for (Recipe recipe : recipes) {
            builder.append(recipe.id).append(" | ").append(recipe.name).append(" | 我自己的菜谱");
            if (recipe.hasNutrition()) {
                builder.append("，约 ").append(recipe.kcal).append("kcal、蛋白 ")
                        .append(recipe.proteinG).append("g");
            }
            if (!recipe.tags.isEmpty()) {
                builder.append("，口味:").append(join(recipe.tags));
            }
            if (recipe.rating > 0) {
                builder.append("，我给 ").append(recipe.rating).append(" 星");
            }
            if (recipe.review.length() > 0) {
                String review = recipe.review.length() > 40
                        ? recipe.review.substring(0, 40) : recipe.review;
                builder.append("，点评:").append(review);
            }
            builder.append("\n");
        }
        for (BuiltinRecipe builtin : builtinRecipes) {
            if (savedCopyOfBuiltin(builtin.id()) != null) {
                continue;   // 已收进我的菜谱，上面那份已经列过
            }
            builder.append(builtin.id()).append(" | ").append(builtin.name())
                    .append(" | 循证食谱，").append(join(builtin.mealSlots())).append("，")
                    .append(builtin.macroLabel());
            if (!builtin.tags().isEmpty()) {
                builder.append("，").append(join(builtin.tags()));
            }
            builder.append("\n");
        }
        builder.append("只返回 JSON：{\"id\": \"选中的 id\", \"reason\": \"一句话中文说明，"
                + "要点出它补了哪个缺口或为什么热量合适\"}。id 必须是上面出现过的。");
        return builder.toString();
    }

    /** 把 AI 选中的 id 落到我的菜谱或循证食谱上；id 对不上返回 false，让调用方退回本地推荐。 */
    private boolean applyFoodAiPick(String text) {
        try {
            JSONObject object = new JSONObject(text);
            String id = object.optString("id", "").trim();
            String reason = object.optString("reason", "").trim();
            Recipe mine = recipeById(id);
            if (mine != null) {
                clearRecommendation();
                recommendedRecipeId = mine.id;
                recommendedRecipeReason = reason;
                return true;
            }
            BuiltinRecipe builtin = builtinRecipeById(id);
            if (builtin != null) {
                clearRecommendation();
                scienceRecId = builtin.id();
                scienceRecReason = reason.length() == 0 ? "与今日营养目标匹配" : "推荐理由：" + reason;
                return true;
            }
            return false;
        } catch (Exception ignored) {
            return false;
        }
    }

    private Recipe pickRecipe(String pref, String excludeId) {
        List<Recipe> pool = new ArrayList<Recipe>(recipes);
        final Map<String, Integer> scores = new HashMap<String, Integer>();
        if (pref != null && pref.length() > 0) {
            boolean matched = false;
            for (Recipe recipe : pool) {
                int score = matchScore(recipe, pref);
                if (score > 0) {
                    matched = true;
                }
                scores.put(recipe.id, score);
            }
            if (matched) {
                List<Recipe> filtered = new ArrayList<Recipe>();
                for (Recipe recipe : pool) {
                    if (scores.get(recipe.id) > 0) {
                        filtered.add(recipe);
                    }
                }
                pool = filtered;
            } else {
                Toast.makeText(this, "库内没找到明显匹配，先从高评分菜谱里挑一个", Toast.LENGTH_SHORT).show();
            }
        }
        if (pool.size() > 1 && excludeId != null) {
            for (int i = pool.size() - 1; i >= 0; i--) {
                if (pool.get(i).id.equals(excludeId)) {
                    pool.remove(i);
                }
            }
        }
        if (pool.isEmpty()) {
            return null;
        }
        int totalWeight = 0;
        for (Recipe recipe : pool) {
            totalWeight += recipeWeight(recipe, scores);
        }
        int roll = random.nextInt(Math.max(1, totalWeight));
        for (Recipe recipe : pool) {
            roll -= recipeWeight(recipe, scores);
            if (roll < 0) {
                return recipe;
            }
        }
        return pool.get(pool.size() - 1);
    }

    private int recipeWeight(Recipe recipe, Map<String, Integer> scores) {
        Integer score = scores.get(recipe.id);
        return 1 + recipe.rating + (score == null ? 0 : score * 2);
    }

    private int matchScore(Recipe recipe, String pref) {
        return matchScoreOf(recipe.name, recipe.tags, recipe.note + " " + recipe.review, pref);
    }

    /** 循证食谱也要能按口味匹配，否则「想吃辣的」只对我自己的菜谱生效。 */
    private int matchScore(BuiltinRecipe recipe, String pref) {
        return matchScoreOf(recipe.name(), recipe.tags(), join(recipe.ingredients()), pref);
    }

    private int matchScoreOf(String name, List<String> tags, String extra, String pref) {
        StringBuilder combinedBuilder = new StringBuilder(name);
        for (String tag : tags) {
            combinedBuilder.append(' ').append(tag);
        }
        combinedBuilder.append(' ').append(extra);
        String combined = combinedBuilder.toString();
        int score = 0;
        for (String tag : tags) {
            if (tag.length() > 0 && pref.contains(tag)) {
                score += 3;
            }
        }
        if (name.length() > 0 && pref.contains(name)) {
            score += 5;
        }
        for (String token : pref.split("[，。、,.!？?！:：;；\\s]+")) {
            if (token.length() < 2) {
                continue;
            }
            if (combined.contains(token)) {
                score += 3;
            }
            for (int i = 0; i + 2 <= token.length(); i++) {
                if (combined.contains(token.substring(i, i + 2))) {
                    score += 1;
                }
            }
        }
        return score;
    }

    private Recipe recipeById(String id) {
        if (id == null) {
            return null;
        }
        for (Recipe recipe : recipes) {
            if (recipe.id.equals(id)) {
                return recipe;
            }
        }
        return null;
    }

    private String recipeCover(Recipe recipe) {
        if (!recipe.photos.isEmpty()) {
            return recipe.photos.get(0);
        }
        return recipe.sourceMedia;
    }

    private String stars(int rating) {
        if (rating <= 0) {
            return "未评分";
        }
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < 5; i++) {
            builder.append(i < rating ? "★" : "☆");
        }
        return builder.toString();
    }

    private View recommendedCard(final Recipe recipe) {
        boolean fromWeb = !isLibraryRecipe(recipe) && recipe.sourceUrl.length() > 0;
        boolean hasReason = recommendedRecipeReason.length() > 0;
        LinearLayout card = card();
        card.addView(smallLabel(fromWeb ? "联网找到" : (hasReason ? "按今日缺口推荐" : "今日推荐")));
        card.addView(space(6));
        card.addView(recipeImage(recipeCover(recipe), 170));
        card.addView(space(8));
        card.addView(text(recipe.name, 20, Typeface.BOLD, INK));
        card.addView(text(stars(recipe.rating) + (recipe.tags.isEmpty() ? "" : " · " + join(recipe.tags)),
                14, Typeface.BOLD, AMBER));
        if (recipe.hasNutrition()) {
            card.addView(text("约 " + recipe.kcal + " kcal · 蛋白 " + recipe.proteinG
                    + "g · 纤维 " + recipe.fiberG + "g", 13, Typeface.BOLD, BLUE));
        }
        if (hasReason) {
            card.addView(text("推荐理由：" + recommendedRecipeReason, 13, Typeface.NORMAL, GREEN));
        }
        if (fromWeb) {
            String site = RecipeSources.labelFor(recipe.sourceUrl);
            card.addView(externalLinkText("来源：" + (site.length() > 0 ? site + " · " : "")
                    + recipe.sourceUrl, recipe.sourceUrl, 12));
        }
        if (recipe.review.length() > 0) {
            card.addView(text("点评：" + recipe.review, 13, Typeface.NORMAL, MUTED));
        }
        card.addView(space(10));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(button("就吃这个", GREEN, Color.WHITE, v -> renderRecipeDetail(recipe)),
                new LinearLayout.LayoutParams(0, dp(44), 1f));
        row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        row.addView(button("换一个", Color.rgb(236, 240, 234), INK, v -> recommendFood(lastRecommendRandom)),
                new LinearLayout.LayoutParams(0, dp(44), 1f));
        card.addView(row);
        return card;
    }

    private View recipeCard(final Recipe recipe) {
        LinearLayout card = card();
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.addView(recipeImage(recipeCover(recipe), 76), new LinearLayout.LayoutParams(dp(76), dp(76)));
        row.addView(space(12), new LinearLayout.LayoutParams(dp(12), 1));
        LinearLayout texts = new LinearLayout(this);
        texts.setOrientation(LinearLayout.VERTICAL);
        texts.addView(text(recipe.name, 16, Typeface.BOLD, INK));
        if (recipe.builtinId.length() > 0) {
            texts.addView(text("循证 · 已收进我的菜谱", 12, Typeface.BOLD, GREEN));
        }
        texts.addView(text(stars(recipe.rating), 13, Typeface.BOLD, AMBER));
        StringBuilder meta = new StringBuilder();
        if (recipe.hasNutrition()) {
            meta.append(recipe.kcal).append(" kcal · 蛋白 ").append(recipe.proteinG).append("g");
        }
        if (!recipe.tags.isEmpty()) {
            if (meta.length() > 0) {
                meta.append(" · ");
            }
            meta.append(join(recipe.tags));
        }
        if (!recipe.photos.isEmpty()) {
            if (meta.length() > 0) {
                meta.append(" · ");
            }
            meta.append("成品照 ").append(recipe.photos.size()).append(" 张");
        }
        if (meta.length() > 0) {
            texts.addView(text(meta.toString(), 12, Typeface.NORMAL, MUTED));
        }
        row.addView(texts, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        card.addView(row);
        card.setOnClickListener(v -> renderRecipeDetail(recipe));
        card.setOnLongClickListener(v -> {
            showRecipeActions(recipe);
            return true;
        });
        return card;
    }

    private View recipeImage(final String url, int heightDp) {
        FrameLayout frame = new FrameLayout(this);
        frame.setBackground(bg(Color.WHITE, dp(10), Color.rgb(235, 239, 232), 1));
        frame.setLayoutParams(new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(heightDp)));
        final int radius = dp(10);
        frame.setClipToOutline(true);
        frame.setOutlineProvider(new ViewOutlineProvider() {
            @Override
            public void getOutline(View view, Outline outline) {
                outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), radius);
            }
        });
        if (url == null || url.length() == 0) {
            GradientDrawable g = new GradientDrawable(GradientDrawable.Orientation.TL_BR,
                    new int[]{AMBER, darken(AMBER)});
            g.setCornerRadius(radius);
            View fallback = new View(this);
            fallback.setBackground(g);
            frame.addView(fallback, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
            TextView tag = text("菜", 18, Typeface.BOLD, Color.argb(220, 255, 255, 255));
            tag.setGravity(Gravity.CENTER);
            FrameLayout.LayoutParams tlp = new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            tlp.gravity = Gravity.CENTER;
            frame.addView(tag, tlp);
        } else {
            ImageView image = new ImageView(this);
            image.setScaleType(ImageView.ScaleType.CENTER_CROP);
            frame.addView(image, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
            loadThumbInto(image, url);
            frame.setOnClickListener(v -> showPhotoDialog(url));
        }
        return frame;
    }

    private void showPhotoDialog(final String url) {
        ImageView image = new ImageView(this);
        image.setScaleType(ImageView.ScaleType.FIT_CENTER);
        if (isLocalUri(url)) {
            if (!loadLocalImage(image, url)) {
                Toast.makeText(this, "无法打开这张图片", Toast.LENGTH_SHORT).show();
                return;
            }
        } else {
            loadThumbInto(image, url);
        }
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(8), dp(8), dp(8), dp(8));
        box.addView(image, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(320)));
        new AlertDialog.Builder(this)
                .setView(box)
                .setNegativeButton("关闭", null)
                .show();
    }

    private void showRecipeActions(final Recipe recipe) {
        final String[] items = {"查看详情", "评分与点评", "添加成品照", "编辑", "删除菜谱"};
        new AlertDialog.Builder(this)
                .setTitle(recipe.name)
                .setItems(items, (dialog, which) -> {
                    if (which == 0) {
                        renderRecipeDetail(recipe);
                    } else if (which == 1) {
                        showRecipeRating(recipe);
                    } else if (which == 2) {
                        pickRecipePhoto(recipe);
                    } else if (which == 3) {
                        openRecipeEditor(recipe);
                    } else {
                        confirmDeleteRecipe(recipe);
                    }
                })
                .show();
    }

    private void renderRecipeDetail(final Recipe recipe) {
        if (recipe == null) {
            renderFood();
            return;
        }
        currentTab = "food";
        currentRecipeId = recipe.id;
        final boolean inLibrary = isLibraryRecipe(recipe);
        clear();
        content.addView(title(recipe.name, "菜谱详情"));

        LinearLayout head = card();
        head.addView(recipeImage(recipeCover(recipe), 210));
        head.addView(space(10));
        head.addView(text(recipe.name, 22, Typeface.BOLD, INK));
        head.addView(text(stars(recipe.rating) + (recipe.tags.isEmpty() ? "" : " · " + join(recipe.tags)),
                14, Typeface.BOLD, AMBER));
        content.addView(head);

        if (recipe.hasNutrition()) {
            LinearLayout nutrition = card();
            nutrition.addView(section("营养估算（单人份）"));
            nutrition.addView(space(4));
            nutrition.addView(text(recipe.kcal + " kcal · 蛋白 " + recipe.proteinG
                    + "g · 纤维 " + recipe.fiberG + "g", 15, Typeface.BOLD, BLUE));
            if (!recipe.groupGrams.isEmpty()) {
                StringBuilder groups = new StringBuilder();
                for (Map.Entry<FoodGroup, Integer> part : recipe.groupGrams.entrySet()) {
                    if (groups.length() > 0) {
                        groups.append(" · ");
                    }
                    groups.append(part.getKey().label()).append(" ").append(part.getValue()).append("g");
                }
                nutrition.addView(text("宝塔构成：" + groups, 13, Typeface.NORMAL, MUTED));
            }
            nutrition.addView(space(10));
            nutrition.addView(button("我吃了这份 · 记入今日", GREEN, Color.WHITE,
                    v -> markRecipeEaten(recipe)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
            content.addView(nutrition);
        } else if (inLibrary) {
            LinearLayout estimate = card();
            estimate.addView(section("营养估算"));
            estimate.addView(space(4));
            estimate.addView(text("这道菜还没有热量和宝塔估算，所以按缺口推荐时轮不到它，也没法一键记入今日。",
                    13, Typeface.NORMAL, MUTED));
            estimate.addView(space(8));
            estimate.addView(button("用 AI 估算营养", BLUE, Color.WHITE,
                    v -> estimateRecipeNutrition(recipe)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
            content.addView(estimate);
        }

        if (recipe.sourceUrl.length() > 0) {
            LinearLayout source = card();
            source.addView(section("菜谱来源"));
            String site = RecipeSources.labelFor(recipe.sourceUrl);
            if (site.length() > 0) {
                source.addView(text(site, 14, Typeface.BOLD, GREEN));
            }
            source.addView(externalLinkText(recipe.sourceUrl, recipe.sourceUrl, 13));
            source.addView(space(8));
            source.addView(button("在浏览器打开原菜谱", BLUE, Color.WHITE,
                    v -> openExternal(recipe.sourceUrl)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
            content.addView(source);
        }

        if (!recipe.ingredients.isEmpty()) {
            LinearLayout ing = card();
            ing.addView(section("配料"));
            ing.addView(space(4));
            for (int i = 0; i < recipe.ingredients.size(); i++) {
                ing.addView(ingredientRow(recipe.ingredients.get(i), i < recipe.ingredients.size() - 1));
            }
            content.addView(ing);
        }

        if (!recipe.steps.isEmpty()) {
            LinearLayout st = card();
            st.addView(section("做法"));
            st.addView(space(4));
            for (int i = 0; i < recipe.steps.size(); i++) {
                st.addView(stepDetailRow(i + 1, recipe.steps.get(i)));
            }
            content.addView(st);
        } else if (recipe.note.length() > 0) {
            LinearLayout st = card();
            st.addView(section("做法 / 记录"));
            st.addView(text(recipe.note, 15, Typeface.NORMAL, INK));
            content.addView(st);
        }

        if (recipe.review.length() > 0) {
            LinearLayout rv = card();
            rv.addView(section("我的点评"));
            rv.addView(text(recipe.review, 15, Typeface.NORMAL, INK));
            content.addView(rv);
        }

        if (!recipe.photos.isEmpty()) {
            LinearLayout ph = card();
            ph.addView(section("成品照"));
            ph.addView(space(6));
            LinearLayout thumbs = new LinearLayout(this);
            thumbs.setOrientation(LinearLayout.HORIZONTAL);
            for (String url : recipe.photos) {
                View thumb = recipeImage(url, 100);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(dp(100), dp(100));
                lp.setMargins(0, 0, dp(8), 0);
                thumbs.addView(thumb, lp);
            }
            ph.addView(wrapScroll(thumbs));
            content.addView(ph);
        }

        if (inLibrary) {
            LinearLayout row1 = new LinearLayout(this);
            row1.setOrientation(LinearLayout.HORIZONTAL);
            row1.addView(button("评分与点评", GREEN, Color.WHITE, v -> showRecipeRating(recipe)),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            row1.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
            row1.addView(button("添加成品照", BLUE, Color.WHITE, v -> pickRecipePhoto(recipe)),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            content.addView(row1);
            content.addView(space(8));
            LinearLayout row2 = new LinearLayout(this);
            row2.setOrientation(LinearLayout.HORIZONTAL);
            row2.addView(button("编辑", Color.rgb(236, 240, 234), INK, v -> openRecipeEditor(recipe)),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            row2.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
            row2.addView(button("删除", Color.rgb(248, 235, 232), CORAL, v -> confirmDeleteRecipe(recipe)),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            content.addView(row2);
        } else {
            content.addView(button("保存到菜谱库", GREEN, Color.WHITE, v -> saveWebRecipe(recipe)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        }
        content.addView(space(8));
        content.addView(button("← 返回菜谱库", SURFACE, MUTED, v -> renderFood()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        renderBottomNav();
    }

    private boolean isLibraryRecipe(Recipe recipe) {
        return recipe != null && indexOfRecipe(recipe.id) >= 0;
    }

    /** 循证食谱 → 我的菜谱：营养估算、搭配依据和参考文献一起带过去，收进来才有意义。 */
    private Recipe recipeFromBuiltin(BuiltinRecipe builtin) {
        Recipe recipe = new Recipe();
        recipe.id = "recipe_" + System.currentTimeMillis();
        recipe.createdAt = System.currentTimeMillis();
        recipe.name = builtin.name();
        recipe.builtinId = builtin.id();
        recipe.kcal = builtin.kcal();
        recipe.proteinG = builtin.proteinG();
        recipe.fiberG = builtin.fiberG();
        recipe.groupGrams.putAll(builtin.allGroupGrams());
        recipe.tags.addAll(builtin.tags());
        for (String slot : builtin.mealSlots()) {
            if (!recipe.tags.contains(slot)) {
                recipe.tags.add(slot);   // 餐段也当标签，「早餐吃什么」这类说法才匹配得上
            }
        }
        recipe.ingredients.addAll(builtin.ingredients());
        for (String step : builtin.steps()) {
            recipe.steps.add(new RecipeStep(step, ""));
        }
        StringBuilder note = new StringBuilder("为什么这么搭配：").append(builtin.rationale());
        for (String ref : builtin.refs()) {
            note.append("\n· ").append(ref);
        }
        recipe.note = note.toString();
        return recipe;
    }

    /** 这道循证食谱是否已经收进我的菜谱；收过了就不该在列表里出现两次。 */
    private Recipe savedCopyOfBuiltin(String builtinId) {
        if (builtinId == null || builtinId.length() == 0) {
            return null;
        }
        for (Recipe recipe : recipes) {
            if (builtinId.equals(recipe.builtinId)) {
                return recipe;
            }
        }
        return null;
    }

    private void saveBuiltinToLibrary(BuiltinRecipe builtin) {
        Recipe existing = savedCopyOfBuiltin(builtin.id());
        if (existing != null) {
            renderRecipeDetail(existing);
            return;
        }
        Recipe saved = recipeFromBuiltin(builtin);
        recipes.add(0, saved);
        saveState();
        Toast.makeText(this, "已收进我的菜谱，可以评分、加成品照了", Toast.LENGTH_SHORT).show();
        renderRecipeDetail(saved);
    }

    /**
     * 把我的菜谱包成 {@link BuiltinRecipe} 交给 {@link RecipeScorer}，
     * 这样自己的菜和循证食谱用同一把尺子按今日缺口打分，而不是各排各的。
     * 只有填了营养估算的才够格——不知道热量就无从谈「贴合剩余热量」。
     */
    private BuiltinRecipe asScorable(Recipe recipe) {
        return new BuiltinRecipe(recipe.id, recipe.name,
                Arrays.asList("早餐", "午餐", "晚餐", "加餐"), recipe.tags,
                recipe.kcal, recipe.proteinG, 0, 0, recipe.fiberG, recipe.groupGrams,
                recipe.ingredients, Collections.<String>emptyList(),
                "我自己的菜谱", Collections.<String>emptyList(),
                // 自己的菜谱没有训练日标记，跟今天对齐，免得白丢 15 分
                isTrainingDayToday());
    }

    private DailyGap todayGap() {
        return DailyGap.of(energyPlan, pagodaTargets, todayLog());
    }

    /** 循证食谱 + 我的菜谱（有营养估算的）合成一个候选池，按今日缺口统一排序。 */
    private List<RecipeScorer.Scored> rankLibrary(String slot) {
        List<BuiltinRecipe> pool = new ArrayList<BuiltinRecipe>();
        for (BuiltinRecipe builtin : builtinRecipes) {
            if (savedCopyOfBuiltin(builtin.id()) == null) {
                pool.add(builtin);   // 已收进我的菜谱的，用下面那份副本参赛，别重复
            }
        }
        for (Recipe recipe : recipes) {
            if (recipe.hasNutrition()) {
                pool.add(asScorable(recipe));
            }
        }
        DailyGap gap = todayGap();
        return new RecipeScorer().rank(pool, slot, gap.remainingKcal(), gap.remainingProteinG(),
                pagodaTargets, todayLog().gramsByGroup(), isTrainingDayToday());
    }

    private void saveWebRecipe(Recipe recipe) {
        if (recipe == null || isLibraryRecipe(recipe)) {
            return;
        }
        Recipe saved = copyRecipe(recipe);
        saved.id = "recipe_" + System.currentTimeMillis();
        saved.createdAt = System.currentTimeMillis();
        recipes.add(0, saved);
        recommendedWebRecipe = null;
        recommendedRecipeId = saved.id;
        saveState();
        Toast.makeText(this, "已保存到菜谱库", Toast.LENGTH_SHORT).show();
        renderRecipeDetail(saved);
    }

    private View ingredientRow(String item, boolean divider) {
        LinearLayout wrap = new LinearLayout(this);
        wrap.setOrientation(LinearLayout.VERTICAL);
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setPadding(0, dp(7), 0, dp(7));
        String name = item;
        String amount = "";
        int cut = item.lastIndexOf(' ');
        if (cut <= 0) {
            cut = item.lastIndexOf('　');
        }
        if (cut > 0 && cut < item.length() - 1) {
            name = item.substring(0, cut).trim();
            amount = item.substring(cut + 1).trim();
        }
        row.addView(text(name, 15, Typeface.NORMAL, INK),
                new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        if (amount.length() > 0) {
            TextView amt = text(amount, 15, Typeface.NORMAL, MUTED);
            amt.setGravity(Gravity.END);
            row.addView(amt);
        }
        wrap.addView(row);
        if (divider) {
            View line = new View(this);
            line.setBackgroundColor(Color.rgb(238, 241, 236));
            wrap.addView(line, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 1));
        }
        return wrap;
    }

    private View stepDetailRow(int number, RecipeStep step) {
        LinearLayout wrap = new LinearLayout(this);
        wrap.setOrientation(LinearLayout.VERTICAL);
        LinearLayout.LayoutParams wrapLp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        wrapLp.setMargins(0, dp(6), 0, dp(6));
        wrap.setLayoutParams(wrapLp);

        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        TextView num = text(String.valueOf(number), 14, Typeface.BOLD, Color.WHITE);
        num.setGravity(Gravity.CENTER);
        num.setBackground(bg(GREEN, dp(13), GREEN, 0));
        LinearLayout.LayoutParams numLp = new LinearLayout.LayoutParams(dp(26), dp(26));
        numLp.setMargins(0, dp(2), dp(10), 0);
        row.addView(num, numLp);
        row.addView(text(step.text, 15, Typeface.NORMAL, INK),
                new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        wrap.addView(row);
        if (step.image != null && step.image.length() > 0) {
            wrap.addView(space(6));
            View img = recipeImage(step.image, 180);
            LinearLayout.LayoutParams imgLp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, dp(180));
            imgLp.setMargins(dp(36), 0, 0, 0);
            img.setLayoutParams(imgLp);
            wrap.addView(img);
        }
        return wrap;
    }

    private void showRecipeRating(final Recipe recipe) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));

        box.addView(text("评分", 13, Typeface.BOLD, MUTED));
        LinearLayout starRow = new LinearLayout(this);
        starRow.setOrientation(LinearLayout.HORIZONTAL);
        final Button[] starButtons = new Button[5];
        final int[] chosen = {recipe.rating};
        for (int i = 0; i < 5; i++) {
            final int value = i + 1;
            Button star = chip(value + "★", chosen[0] == value, v -> {
                chosen[0] = value;
                for (int j = 0; j < 5; j++) {
                    styleChip(starButtons[j], j + 1 == value);
                }
            });
            starButtons[i] = star;
            starRow.addView(star);
        }
        box.addView(wrapScroll(starRow));

        final EditText review = new EditText(this);
        review.setText(recipe.review);
        review.setHint("点评：味道、火候、下次改进什么（可选）");
        review.setMinLines(3);
        review.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        box.addView(review);

        ScrollView scroll = new ScrollView(this);
        scroll.addView(box);
        new AlertDialog.Builder(this)
                .setTitle("点评 · " + recipe.name)
                .setView(scroll)
                .setNegativeButton("取消", null)
                .setPositiveButton("保存", (dialog, which) -> {
                    recipe.rating = chosen[0];
                    recipe.review = review.getText().toString().trim();
                    saveState();
                    Toast.makeText(this, "已保存点评", Toast.LENGTH_SHORT).show();
                    if ("food".equals(currentTab)) {
                        if (recipe.id.equals(currentRecipeId)) {
                            renderRecipeDetail(recipe);
                        } else {
                            renderFood();
                        }
                    }
                })
                .show();
    }

    private void openRecipeEditor(Recipe existing) {
        editorIsNew = existing == null;
        editorDraft = existing == null ? new Recipe() : copyRecipe(existing);
        if (editorDraft.id.length() == 0) {
            editorDraft.id = "recipe_" + System.currentTimeMillis();
            editorDraft.createdAt = System.currentTimeMillis();
        }
        renderRecipeEditor();
    }

    private void renderRecipeEditor() {
        currentTab = "food";
        clear();
        edIngredientFields.clear();
        edStepFields.clear();
        content.addView(title("菜谱", editorIsNew ? "新建 · 填好后点保存" : "编辑菜谱"));

        LinearLayout coverCard = card();
        coverCard.addView(smallLabel("封面图"));
        coverCard.addView(space(6));
        coverCard.addView(recipeImage(editorDraft.sourceMedia, 150));
        coverCard.addView(space(8));
        LinearLayout coverRow = new LinearLayout(this);
        coverRow.setOrientation(LinearLayout.HORIZONTAL);
        coverRow.addView(button(editorDraft.sourceMedia.length() > 0 ? "换封面图" : "选封面图",
                Color.rgb(236, 240, 234), INK, v -> pickCover()),
                new LinearLayout.LayoutParams(0, dp(42), 1f));
        if (editorDraft.sourceMedia.length() > 0) {
            coverRow.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
            coverRow.addView(button("移除", Color.rgb(248, 235, 232), CORAL, v -> {
                harvestEditor();
                editorDraft.sourceMedia = "";
                renderRecipeEditor();
            }), new LinearLayout.LayoutParams(0, dp(42), 1f));
        }
        coverCard.addView(coverRow);
        content.addView(coverCard);

        LinearLayout nameCard = card();
        nameCard.addView(smallLabel("菜名"));
        edRecipeName = field("菜名", editorDraft.name, false, 0);
        nameCard.addView(edRecipeName);
        nameCard.addView(space(10));
        LinearLayout tagLabelRow = new LinearLayout(this);
        tagLabelRow.setOrientation(LinearLayout.HORIZONTAL);
        tagLabelRow.setGravity(Gravity.CENTER_VERTICAL);
        tagLabelRow.addView(smallLabel("标签（口味 / 风格）"),
                new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        tagLabelRow.addView(button("AI 自动打标签", GREEN_SOFT, GREEN, v -> aiAutoTags()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(36)));
        nameCard.addView(tagLabelRow);
        edRecipeTags = field("用逗号分开，如：辣、快手、鸡肉", tagsJoined(editorDraft.tags), false, 0);
        nameCard.addView(edRecipeTags);
        content.addView(nameCard);

        LinearLayout ingCard = card();
        ingCard.addView(section("配料 / 调料"));
        ingCard.addView(text("一行一个，右边写用量，如：生抽 2勺", 12, Typeface.NORMAL, MUTED));
        ingCard.addView(space(4));
        for (int i = 0; i < editorDraft.ingredients.size(); i++) {
            final int index = i;
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            EditText f = field("配料 用量", editorDraft.ingredients.get(i), false, 0);
            edIngredientFields.add(f);
            row.addView(f, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            row.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
            row.addView(button("✕", Color.rgb(248, 235, 232), CORAL, v -> {
                harvestEditor();
                if (index < editorDraft.ingredients.size()) {
                    editorDraft.ingredients.remove(index);
                }
                renderRecipeEditor();
            }), new LinearLayout.LayoutParams(dp(44), dp(44)));
            ingCard.addView(row);
        }
        ingCard.addView(space(6));
        ingCard.addView(button("＋ 加一行配料", Color.rgb(236, 240, 234), INK, v -> {
            harvestEditor();
            editorDraft.ingredients.add("");
            renderRecipeEditor();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        content.addView(ingCard);

        LinearLayout stepCard = card();
        stepCard.addView(section("做法步骤"));
        stepCard.addView(text("一步一段，可给每步单独配图", 12, Typeface.NORMAL, MUTED));
        stepCard.addView(space(4));
        for (int i = 0; i < editorDraft.steps.size(); i++) {
            final int index = i;
            RecipeStep step = editorDraft.steps.get(i);
            LinearLayout block = new LinearLayout(this);
            block.setOrientation(LinearLayout.VERTICAL);
            LinearLayout.LayoutParams blockLp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            blockLp.setMargins(0, dp(6), 0, dp(6));
            block.setLayoutParams(blockLp);

            LinearLayout headRow = new LinearLayout(this);
            headRow.setOrientation(LinearLayout.HORIZONTAL);
            headRow.setGravity(Gravity.CENTER_VERTICAL);
            headRow.addView(text("第 " + (i + 1) + " 步", 14, Typeface.BOLD, GREEN),
                    new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            headRow.addView(button("删除此步", Color.rgb(248, 235, 232), CORAL, v -> {
                harvestEditor();
                if (index < editorDraft.steps.size()) {
                    editorDraft.steps.remove(index);
                }
                renderRecipeEditor();
            }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(36)));
            block.addView(headRow);

            EditText f = field("这一步怎么做（火候、时间等）", step.text, true, 78);
            edStepFields.add(f);
            block.addView(f);

            if (step.image != null && step.image.length() > 0) {
                block.addView(space(6));
                block.addView(recipeImage(step.image, 150));
                block.addView(space(4));
                LinearLayout imgRow = new LinearLayout(this);
                imgRow.setOrientation(LinearLayout.HORIZONTAL);
                imgRow.addView(button("换配图", Color.rgb(236, 240, 234), INK, v -> pickStepImage(index)),
                        new LinearLayout.LayoutParams(0, dp(40), 1f));
                imgRow.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
                imgRow.addView(button("移除配图", Color.rgb(248, 235, 232), CORAL, v -> {
                    harvestEditor();
                    if (index < editorDraft.steps.size()) {
                        editorDraft.steps.get(index).image = "";
                    }
                    renderRecipeEditor();
                }), new LinearLayout.LayoutParams(0, dp(40), 1f));
                block.addView(imgRow);
            } else {
                block.addView(space(4));
                block.addView(button("＋ 步骤配图", Color.rgb(236, 240, 234), INK, v -> pickStepImage(index)),
                        new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(40)));
            }
            View line = new View(this);
            line.setBackgroundColor(Color.rgb(238, 241, 236));
            LinearLayout.LayoutParams lineLp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 1);
            lineLp.setMargins(0, dp(8), 0, 0);
            block.addView(line, lineLp);
            stepCard.addView(block);
        }
        stepCard.addView(space(6));
        stepCard.addView(button("＋ 加一步", Color.rgb(236, 240, 234), INK, v -> {
            harvestEditor();
            editorDraft.steps.add(new RecipeStep());
            renderRecipeEditor();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        content.addView(stepCard);

        LinearLayout reviewCard = card();
        reviewCard.addView(smallLabel("我的点评（可选）"));
        edRecipeReview = field("味道、火候、下次改进什么", editorDraft.review, true, 90);
        reviewCard.addView(edRecipeReview);
        content.addView(reviewCard);

        LinearLayout saveRow = new LinearLayout(this);
        saveRow.setOrientation(LinearLayout.HORIZONTAL);
        saveRow.addView(button("保存菜谱", GREEN, Color.WHITE, v -> saveEditor()),
                new LinearLayout.LayoutParams(0, dp(50), 2f));
        saveRow.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        saveRow.addView(button("取消", Color.rgb(236, 240, 234), INK, v -> {
            editorDraft = null;
            renderFood();
        }), new LinearLayout.LayoutParams(0, dp(50), 1f));
        content.addView(saveRow);
        renderBottomNav();
    }

    private EditText field(String hint, String value, boolean multiline, int heightDp) {
        EditText edit = new EditText(this);
        edit.setHint(hint);
        edit.setText(value == null ? "" : value);
        edit.setTextColor(INK);
        edit.setHintTextColor(Color.rgb(150, 158, 153));
        edit.setTextSize(15);
        edit.setBackground(bg(Color.rgb(249, 251, 247), dp(8), LINE, 1));
        edit.setPadding(dp(12), dp(10), dp(12), dp(10));
        if (multiline) {
            edit.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
            edit.setGravity(Gravity.TOP | Gravity.START);
        } else {
            edit.setSingleLine(true);
        }
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                heightDp > 0 ? dp(heightDp) : ViewGroup.LayoutParams.WRAP_CONTENT);
        lp.setMargins(0, dp(4), 0, 0);
        edit.setLayoutParams(lp);
        return edit;
    }

    private String tagsJoined(List<String> tags) {
        StringBuilder builder = new StringBuilder();
        for (String tag : tags) {
            if (builder.length() > 0) {
                builder.append("、");
            }
            builder.append(tag);
        }
        return builder.toString();
    }

    private void harvestEditor() {
        if (editorDraft == null) {
            return;
        }
        if (edRecipeName != null) {
            editorDraft.name = edRecipeName.getText().toString().trim();
        }
        if (edRecipeReview != null) {
            editorDraft.review = edRecipeReview.getText().toString().trim();
        }
        if (edRecipeTags != null) {
            editorDraft.tags.clear();
            for (String tag : edRecipeTags.getText().toString().split("[，、,;；\\s]+")) {
                String trimmed = tag.trim();
                if (trimmed.length() > 0 && !editorDraft.tags.contains(trimmed)) {
                    editorDraft.tags.add(trimmed);
                }
            }
        }
        for (int i = 0; i < edIngredientFields.size() && i < editorDraft.ingredients.size(); i++) {
            editorDraft.ingredients.set(i, edIngredientFields.get(i).getText().toString().trim());
        }
        for (int i = 0; i < edStepFields.size() && i < editorDraft.steps.size(); i++) {
            editorDraft.steps.get(i).text = edStepFields.get(i).getText().toString().trim();
        }
    }

    private void saveEditor() {
        harvestEditor();
        if (editorDraft == null) {
            renderFood();
            return;
        }
        if (editorDraft.name.length() == 0) {
            Toast.makeText(this, "菜名不能为空", Toast.LENGTH_SHORT).show();
            return;
        }
        for (int i = editorDraft.ingredients.size() - 1; i >= 0; i--) {
            if (editorDraft.ingredients.get(i).trim().length() == 0) {
                editorDraft.ingredients.remove(i);
            }
        }
        for (int i = editorDraft.steps.size() - 1; i >= 0; i--) {
            RecipeStep step = editorDraft.steps.get(i);
            if (step.text.trim().length() == 0 && step.image.length() == 0) {
                editorDraft.steps.remove(i);
            }
        }
        int index = indexOfRecipe(editorDraft.id);
        if (index >= 0) {
            recipes.set(index, editorDraft);
        } else {
            recipes.add(0, editorDraft);
        }
        Recipe saved = editorDraft;
        editorDraft = null;
        saveState();
        Toast.makeText(this, editorIsNew ? "已加入菜谱库" : "已更新菜谱", Toast.LENGTH_SHORT).show();
        renderRecipeDetail(saved);
    }

    private Recipe copyRecipe(Recipe src) {
        Recipe copy = new Recipe();
        copy.id = src.id;
        copy.name = src.name;
        copy.sourceMedia = src.sourceMedia;
        copy.sourceUrl = src.sourceUrl;
        copy.note = src.note;
        copy.review = src.review;
        copy.rating = src.rating;
        copy.createdAt = src.createdAt;
        copy.builtinId = src.builtinId;
        copy.kcal = src.kcal;
        copy.proteinG = src.proteinG;
        copy.fiberG = src.fiberG;
        copy.groupGrams.putAll(src.groupGrams);
        copy.tags.addAll(src.tags);
        copy.photos.addAll(src.photos);
        copy.ingredients.addAll(src.ingredients);
        for (RecipeStep step : src.steps) {
            copy.steps.add(new RecipeStep(step.text, step.image));
        }
        return copy;
    }

    private int indexOfRecipe(String id) {
        for (int i = 0; i < recipes.size(); i++) {
            if (recipes.get(i).id.equals(id)) {
                return i;
            }
        }
        return -1;
    }

    private void confirmDeleteRecipe(final Recipe recipe) {
        new AlertDialog.Builder(this)
                .setTitle("删除菜谱？")
                .setMessage("「" + recipe.name + "」和它的点评、照片记录都会删除，无法恢复。")
                .setNegativeButton("取消", null)
                .setPositiveButton("删除", (dialog, which) -> {
                    int index = indexOfRecipe(recipe.id);
                    if (index >= 0) {
                        recipes.remove(index);
                    }
                    if (recipe.id.equals(recommendedRecipeId)) {
                        recommendedRecipeId = null;
                    }
                    if (recipe.id.equals(currentRecipeId)) {
                        currentRecipeId = null;
                    }
                    saveState();
                    Toast.makeText(this, "已删除菜谱「" + recipe.name + "」", Toast.LENGTH_SHORT).show();
                    if ("food".equals(currentTab)) {
                        renderFood();
                    }
                })
                .show();
    }

    private void pickRecipeImport() {
        if (!aiConfigured()) {
            promptEnableAi("图片识别");
            return;
        }
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("image/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivityForResult(intent, REQ_PICK_RECIPE_IMPORT);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开图片选择器", Toast.LENGTH_SHORT).show();
        }
    }

    private void pickCover() {
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("image/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivityForResult(intent, REQ_PICK_RECIPE_COVER);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开图片选择器", Toast.LENGTH_SHORT).show();
        }
    }

    private void pickStepImage(int index) {
        pendingStepIndex = index;
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("image/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivityForResult(intent, REQ_PICK_STEP_IMAGE);
        } catch (Exception ignored) {
            pendingStepIndex = -1;
            Toast.makeText(this, "无法打开图片选择器", Toast.LENGTH_SHORT).show();
        }
    }

    private void askRecipeLink() {
        if (!webSearchConfigured() && !aiConfigured()) {
            promptEnableAi("链接解析");
            return;
        }
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));
        box.addView(text("粘贴一个菜谱链接，AI 会抓取网页里的配料和步骤。", 13, Typeface.NORMAL, MUTED));
        final EditText input = new EditText(this);
        input.setHint("https://…");
        input.setSingleLine(true);
        box.addView(input);
        new AlertDialog.Builder(this)
                .setTitle("从链接解析菜谱")
                .setView(box)
                .setNegativeButton("取消", null)
                .setPositiveButton("解析", (dialog, which) -> {
                    String url = input.getText().toString().trim();
                    if (!isWebUrl(url)) {
                        Toast.makeText(this, "请输入 http/https 链接", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    importRecipeFromLink(url);
                })
                .show();
    }

    private void importRecipeFromImage(final Uri uri) {
        PreparedImage image = prepareImageForAi(uri);
        if (image == null) {
            Toast.makeText(this, "无法读取这张图片", Toast.LENGTH_SHORT).show();
            return;
        }
        final String source = uri.toString();
        final AlertDialog busy = showBusy("AI 正在识别菜谱…");
        geminiClient.generate(aiApiKey, aiModel, recipeExtractionPrompt(), image.bytes, image.mimeType,
                new GeminiClient.Callback() {
                    @Override
                    public void onResult(String text) {
                        busy.dismiss();
                        Recipe draft = parseExtractedRecipe(text);
                        if (draft != null) {
                            draft.sourceMedia = source;
                            applyExtractedRecipe(draft, "已识别，请核对后保存");
                        } else {
                            Recipe blank = new Recipe();
                            blank.sourceMedia = source;
                            applyExtractedRecipe(blank, "没能识别出内容，改成手动录入");
                        }
                    }

                    @Override
                    public void onError(String message) {
                        busy.dismiss();
                        Recipe blank = new Recipe();
                        blank.sourceMedia = source;
                        applyExtractedRecipe(blank, "识别失败（" + message + "），改成手动录入");
                    }
                });
    }

    private void importRecipeFromLink(final String url) {
        final AlertDialog busy = showBusy("正在抓取并解析链接…");
        String prompt = recipeExtractionPrompt() + "\n\n请使用联网访问工具直接读取这个公开菜谱链接：" + url;
        generateUrlWithWebProvider(prompt, new GeminiClient.Callback() {
            @Override
            public void onModelFallback(String requestedModel, String fallbackModel) {
                persistWebSearchModelFallback(requestedModel, fallbackModel);
            }

            @Override
            public void onResult(String text) {
                Recipe draft = parseExtractedRecipe(text);
                if (draft != null) {
                    busy.dismiss();
                    draft.sourceUrl = url;
                    applyExtractedRecipe(draft, "已从链接解析，请核对后保存");
                } else {
                    fallbackFetchRecipeLink(url, busy);
                }
            }

            @Override
            public void onError(String message) {
                fallbackFetchRecipeLink(url, busy);
            }
        });
    }

    private void fallbackFetchRecipeLink(final String url, final AlertDialog busy) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                String pageText;
                try {
                    pageText = fetchReadableText(url);
                } catch (Exception e) {
                    pageText = null;
                }
                final String content = pageText;
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        if (content == null || content.length() < 30) {
                            busy.dismiss();
                            Toast.makeText(MainActivity.this,
                                    "读取不到这个链接的内容，可改用图片识别或手动录入", Toast.LENGTH_LONG).show();
                            return;
                        }
                        String prompt = recipeExtractionPrompt() + "\n\n网页内容：\n"
                                + (content.length() > 6000 ? content.substring(0, 6000) : content);
                        geminiClient.generate(aiApiKey, aiModel, prompt, new GeminiClient.Callback() {
                            @Override
                            public void onResult(String text) {
                                busy.dismiss();
                                Recipe draft = parseExtractedRecipe(text);
                                if (draft != null) {
                                    draft.sourceUrl = url;
                                    applyExtractedRecipe(draft, "已从链接解析，请核对后保存");
                                } else {
                                    Toast.makeText(MainActivity.this,
                                            "没能从链接解析出菜谱", Toast.LENGTH_LONG).show();
                                }
                            }

                            @Override
                            public void onError(String message) {
                                busy.dismiss();
                                Toast.makeText(MainActivity.this,
                                        "解析失败：" + message, Toast.LENGTH_LONG).show();
                            }
                        });
                    }
                });
            }
        }).start();
    }

    private String fetchReadableText(String url) throws Exception {
        java.net.HttpURLConnection conn = (java.net.HttpURLConnection) new java.net.URL(url).openConnection();
        conn.setConnectTimeout(12000);
        conn.setReadTimeout(15000);
        conn.setInstanceFollowRedirects(true);
        conn.setRequestProperty("User-Agent",
                "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36");
        conn.setRequestProperty("Accept", "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8");
        conn.setRequestProperty("Accept-Encoding", "identity");
        conn.connect();
        int code = conn.getResponseCode();
        if (code < 200 || code >= 300) {
            conn.disconnect();
            throw new java.io.IOException("链接返回 HTTP " + code);
        }
        java.io.InputStream is = conn.getInputStream();
        byte[] data = readUpTo(is, 2 * 1024 * 1024);
        is.close();
        String contentType = conn.getContentType();
        conn.disconnect();
        String charset = "UTF-8";
        if (contentType != null) {
            String lower = contentType.toLowerCase(Locale.ROOT);
            if (lower.contains("gb2312") || lower.contains("gbk") || lower.contains("gb18030")) {
                charset = "GBK";
            }
        }
        String html = new String(data, charset);
        String structured = extractRecipeStructuredData(html);
        html = html.replaceAll("(?is)<script.*?</script>", " ")
                .replaceAll("(?is)<style.*?</style>", " ")
                .replaceAll("(?is)<[^>]+>", " ")
                .replaceAll("&nbsp;|&#160;", " ")
                .replaceAll("[ \\t\\x0B\\f\\r]+", " ")
                .replaceAll("\\n\\s*\\n+", "\n");
        html = decodeBasicHtmlEntities(html).trim();
        return (structured.length() > 0 ? "网页内的结构化菜谱数据：\n" + structured + "\n\n网页正文：\n" : "") + html;
    }

    private byte[] readUpTo(java.io.InputStream is, int maxBytes) throws java.io.IOException {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        byte[] buffer = new byte[8192];
        int read;
        int total = 0;
        while ((read = is.read(buffer)) != -1) {
            int allowed = Math.min(read, maxBytes - total);
            if (allowed > 0) {
                out.write(buffer, 0, allowed);
                total += allowed;
            }
            if (total >= maxBytes) {
                break;
            }
        }
        return out.toByteArray();
    }

    private String extractRecipeStructuredData(String html) {
        StringBuilder result = new StringBuilder();
        java.util.regex.Matcher matcher = java.util.regex.Pattern.compile(
                "(?is)<script[^>]*type\\s*=\\s*['\"]application/ld\\+json['\"][^>]*>(.*?)</script>")
                .matcher(html);
        while (matcher.find() && result.length() < 12000) {
            String block = decodeBasicHtmlEntities(matcher.group(1)).trim();
            if (block.contains("Recipe") || block.contains("recipeIngredient")
                    || block.contains("recipeInstructions")) {
                if (result.length() > 0) {
                    result.append('\n');
                }
                result.append(block.length() > 6000 ? block.substring(0, 6000) : block);
            }
        }
        return result.toString();
    }

    private String decodeBasicHtmlEntities(String value) {
        return value.replace("&nbsp;", " ")
                .replace("&#160;", " ")
                .replace("&amp;", "&")
                .replace("&quot;", "\"")
                .replace("&#39;", "'")
                .replace("&lt;", "<")
                .replace("&gt;", ">");
    }

    private String recipeExtractionPrompt() {
        return "你是做饭助手。请从我给你的菜谱（图片或网页文字）里提取结构化信息。"
                + "图片可能是菜谱截图、手写菜谱、菜品成品照或包含多段文字的长图，请先仔细识别所有可见文字和菜品内容。"
                + "只返回 JSON，不要多余文字。\n"
                + "格式：{\"name\":\"菜名\",\"tags\":[\"口味或风格，如 辣/家常/快手\"],"
                + "\"ingredients\":[\"配料名 用量，如 生抽 2勺\"],"
                + "\"steps\":[\"第一步做法\",\"第二步做法\"],"
                + "\"kcal\":单人份热量整数,\"protein_g\":蛋白克数整数,\"fiber_g\":纤维克数整数,"
                + "\"pagoda_grams\":{类别:生重克数}}\n"
                + "要求：配料要尽量包含调料及用量；步骤按顺序、每步一句话、保留火候和时间等关键信息；"
                + "tags 由你根据菜品自动归纳 2-4 个。"
                + "营养按《中国食物成分表》常见值估算单人份，pagoda_grams 的类别只能用这些键："
                + pagodaKeyList() + "；一律填生重/干重（一碗熟米饭记 GRAIN 80，不是熟重 200），"
                + "没有的类别就不要写。识别不到的字段就给空数组或空字符串。";
    }

    private Recipe parseExtractedRecipe(String text) {
        try {
            return recipeFromAiObject(new JSONObject(text));
        } catch (Exception ignored) {
            return null;
        }
    }

    private Recipe recipeFromAiObject(JSONObject object) {
        Recipe recipe = new Recipe();
        recipe.id = "recipe_" + System.currentTimeMillis();
        recipe.createdAt = System.currentTimeMillis();
        recipe.name = object.optString("name", "").trim();
        JSONArray tags = object.optJSONArray("tags");
        if (tags != null) {
            for (int i = 0; i < tags.length(); i++) {
                String tag = tags.optString(i).trim();
                if (tag.length() > 0 && !recipe.tags.contains(tag)) {
                    recipe.tags.add(tag);
                }
            }
        }
        JSONArray ingredients = object.optJSONArray("ingredients");
        if (ingredients != null) {
            for (int i = 0; i < ingredients.length(); i++) {
                String item = ingredients.optString(i).trim();
                if (item.length() > 0) {
                    recipe.ingredients.add(item);
                }
            }
        }
        JSONArray steps = object.optJSONArray("steps");
        if (steps != null) {
            for (int i = 0; i < steps.length(); i++) {
                JSONObject stepObject = steps.optJSONObject(i);
                String stepText = stepObject != null ? stepObject.optString("text") : steps.optString(i);
                if (stepText != null && stepText.trim().length() > 0) {
                    recipe.steps.add(new RecipeStep(stepText.trim(), ""));
                }
            }
        }
        recipe.kcal = Math.max(0, object.optInt("kcal", 0));
        recipe.proteinG = Math.max(0, object.optInt("protein_g", 0));
        recipe.fiberG = Math.max(0, object.optInt("fiber_g", 0));
        JSONObject pagoda = object.optJSONObject("pagoda_grams");
        if (pagoda != null) {
            for (FoodGroup group : FoodGroup.values()) {
                int grams = pagoda.optInt(group.name(), 0);
                if (grams > 0) {
                    recipe.groupGrams.put(group, grams);
                }
            }
        }
        if (recipe.name.length() == 0 || (recipe.ingredients.isEmpty() && recipe.steps.isEmpty())) {
            return null;
        }
        return recipe;
    }

    /** 宝塔类别的键名清单，写进提示词，免得 AI 自己造键名。 */
    private String pagodaKeyList() {
        StringBuilder builder = new StringBuilder();
        for (FoodGroup group : FoodGroup.values()) {
            if (builder.length() > 0) {
                builder.append("、");
            }
            builder.append(group.name()).append("=").append(group.label());
        }
        return builder.toString();
    }

    private void applyExtractedRecipe(Recipe draft, String toastMessage) {
        editorDraft = draft;
        editorIsNew = true;
        if (editorDraft.id.length() == 0) {
            editorDraft.id = "recipe_" + System.currentTimeMillis();
            editorDraft.createdAt = System.currentTimeMillis();
        }
        if (toastMessage != null) {
            Toast.makeText(this, toastMessage, Toast.LENGTH_LONG).show();
        }
        renderRecipeEditor();
    }

    private void aiAutoTags() {
        if (!aiConfigured()) {
            promptEnableAi("AI 标签");
            return;
        }
        harvestEditor();
        if (editorDraft.name.length() == 0 && editorDraft.ingredients.isEmpty()) {
            Toast.makeText(this, "先填一下菜名或配料", Toast.LENGTH_SHORT).show();
            return;
        }
        final AlertDialog busy = showBusy("AI 正在打标签…");
        StringBuilder prompt = new StringBuilder();
        prompt.append("根据下面这道菜，归纳 2-4 个中文标签（口味/风格/主料），只返回 JSON：{\"tags\":[\"...\"]}。\n");
        prompt.append("菜名：").append(editorDraft.name).append("\n");
        if (!editorDraft.ingredients.isEmpty()) {
            prompt.append("配料：").append(join(editorDraft.ingredients)).append("\n");
        }
        geminiClient.generate(aiApiKey, aiModel, prompt.toString(), new GeminiClient.Callback() {
            @Override
            public void onResult(String text) {
                busy.dismiss();
                try {
                    JSONArray tags = new JSONObject(text).optJSONArray("tags");
                    if (tags != null) {
                        editorDraft.tags.clear();
                        for (int i = 0; i < tags.length(); i++) {
                            String tag = tags.optString(i).trim();
                            if (tag.length() > 0 && !editorDraft.tags.contains(tag)) {
                                editorDraft.tags.add(tag);
                            }
                        }
                    }
                } catch (Exception ignored) {
                    // Keep existing tags if parsing fails.
                }
                Toast.makeText(MainActivity.this, "已生成标签", Toast.LENGTH_SHORT).show();
                renderRecipeEditor();
            }

            @Override
            public void onError(String message) {
                busy.dismiss();
                Toast.makeText(MainActivity.this, "生成标签失败：" + message, Toast.LENGTH_LONG).show();
            }
        });
    }

    private PreparedImage prepareImageForAi(Uri uri) {
        try {
            java.io.InputStream is = getContentResolver().openInputStream(uri);
            byte[] raw = readAllBytes(is);
            if (is != null) {
                is.close();
            }
            String mime = getContentResolver().getType(uri);
            if (mime != null) {
                mime = mime.toLowerCase(Locale.ROOT);
            }
            boolean supported = "image/png".equals(mime) || "image/jpeg".equals(mime)
                    || "image/webp".equals(mime) || "image/heic".equals(mime) || "image/heif".equals(mime);
            // Preserve screenshot text and fine food details whenever the inline request stays modest.
            if (supported && raw.length <= 10 * 1024 * 1024) {
                return new PreparedImage(raw, mime);
            }

            BitmapFactory.Options bounds = new BitmapFactory.Options();
            bounds.inJustDecodeBounds = true;
            BitmapFactory.decodeByteArray(raw, 0, raw.length, bounds);
            if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
                return null;
            }
            int sample = 1;
            while (((long) bounds.outWidth * bounds.outHeight) / (sample * sample) > 8_000_000L
                    || Math.max(bounds.outWidth, bounds.outHeight) / sample > 5000) {
                sample *= 2;
            }
            BitmapFactory.Options opts = new BitmapFactory.Options();
            opts.inSampleSize = sample;
            Bitmap bitmap = BitmapFactory.decodeByteArray(raw, 0, raw.length, opts);
            if (bitmap == null) {
                return null;
            }
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
            bitmap.recycle();
            return new PreparedImage(out.toByteArray(), "image/jpeg");
        } catch (Exception ignored) {
            return null;
        }
    }

    private AlertDialog showBusy(String message) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.HORIZONTAL);
        box.setPadding(dp(22), dp(22), dp(22), dp(22));
        box.setGravity(Gravity.CENTER_VERTICAL);
        android.widget.ProgressBar bar = new android.widget.ProgressBar(this);
        box.addView(bar, new LinearLayout.LayoutParams(dp(34), dp(34)));
        box.addView(space(14), new LinearLayout.LayoutParams(dp(14), 1));
        box.addView(text(message, 15, Typeface.BOLD, INK));
        AlertDialog dialog = new AlertDialog.Builder(this)
                .setView(box)
                .setCancelable(false)
                .create();
        dialog.show();
        return dialog;
    }

    private void promptEnableAi(String feature) {
        new AlertDialog.Builder(this)
                .setTitle(feature + "需要 AI")
                .setMessage("请先在「设置 → AI 推荐」里开启 AI，并为该功能填入 Gemini 或 Groq API Key。")
                .setNegativeButton("以后再说", null)
                .setPositiveButton("去设置", (dialog, which) -> renderSettings())
                .show();
    }

    private void pickRecipePhoto(Recipe recipe) {
        pendingRecipePhotoId = recipe.id;
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("image/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivityForResult(intent, REQ_PICK_RECIPE_PHOTO);
        } catch (Exception ignored) {
            pendingRecipePhotoId = null;
            Toast.makeText(this, "无法打开图片选择器", Toast.LENGTH_SHORT).show();
        }
    }

    private View painRow(String label, PainSeverity current, SeveritySetter setter) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(0, dp(8), 0, dp(8));
        box.addView(text(label + "：" + (current == null ? "无" : current.label()), 15, Typeface.BOLD, INK));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        addPainChip(row, "无", current == null, v -> setter.set(null));
        addPainChip(row, "轻微", current == PainSeverity.MILD, v -> setter.set(PainSeverity.MILD));
        addPainChip(row, "明显", current == PainSeverity.MODERATE, v -> setter.set(PainSeverity.MODERATE));
        addPainChip(row, "急性", current == PainSeverity.SEVERE, v -> setter.set(PainSeverity.SEVERE));
        box.addView(row);
        return box;
    }

    private void addPainChip(LinearLayout row, String label, boolean selected, View.OnClickListener listener) {
        row.addView(chip(label, selected, listener), new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, dp(38)));
    }

    private LinearLayout intensityRow() { return intensityRow(false); }

    private LinearLayout intensityRow(boolean defaults) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        final Intensity[] options = {Intensity.LOW, Intensity.MEDIUM, Intensity.HIGH};
        final Button[] chips = new Button[options.length];
        for (int i = 0; i < options.length; i++) {
            final Intensity intensity = options[i];
            Button c = chip(intensity.label(), (defaults ? defaultIntensity : selectedIntensity) == intensity, v -> {
                if (defaults) {
                    defaultIntensity = intensity;
                    if (customIntensityOverride == null) selectedIntensity = intensity;
                    if (quickIntensityOverride == null) quickGentle = intensity == Intensity.LOW;
                } else {
                    customIntensityOverride = intensity;
                    selectedIntensity = intensity;
                }
                saveState();
                for (int j = 0; j < options.length; j++) {
                    styleChip(chips[j], options[j] == (defaults ? defaultIntensity : selectedIntensity));
                }
                updateStatusCard();
                if (!defaults) {
                    commandDraft = commandInput.getText().toString();
                    renderAdHocSetup();
                }
            });
            chips[i] = c;
            row.addView(c);
        }
        return row;
    }

    private View durationRow() {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        final int[] options = {5, 15, 25, 40, 0};
        final Button[] chips = new Button[options.length];
        for (int i = 0; i < options.length; i++) {
            final int minutes = options[i];
            Button c = chip(minutes == 0 ? "不限时" : minutes + "分", selectedDurationMinutes == minutes, v -> {
                selectedDurationMinutes = minutes;
                saveState();
                for (int j = 0; j < options.length; j++) {
                    styleChip(chips[j], options[j] == selectedDurationMinutes);
                }
                updateStatusCard();
            });
            c.setSingleLine(true);
            c.setTextSize(13);
            c.setMinWidth(dp(58));
            chips[i] = c;
            row.addView(c);
        }
        HorizontalScrollView scroll = new HorizontalScrollView(this);
        scroll.setHorizontalScrollBarEnabled(false);
        scroll.addView(row);
        return scroll;
    }

    private void updateStatusCard() {
        if (statusLine != null) {
            statusLine.setText(selectedIntensity.label() + "强度 · " + durationLabel(selectedDurationMinutes) + " · 器械 " + equipment.size()
                    + " 项 · 伤痛：" + painSummary());
        }
    }

    private View quickRow(String[] labels) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        for (String label : labels) {
            row.addView(chip(label, false, v -> {
                if ("全身".equals(label)) {
                    commandInput.setText("");
                    generateFromCommand(true);
                } else if ("恢复".equals(label)) {
                    commandInput.setText("恢复");
                    generateFromCommand(false);
                } else {
                    commandInput.setText("我想" + label);
                    generateFromCommand(false);
                }
            }));
        }
        HorizontalScrollView scroll = new HorizontalScrollView(this);
        scroll.setHorizontalScrollBarEnabled(false);
        scroll.addView(row);
        return scroll;
    }

    private void showExerciseDetail(final Exercise exercise) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(18), dp(8), dp(18), dp(4));
        final WebView[] detailWeb = new WebView[1];
        final AlertDialog[] dialogRef = new AlertDialog[1];
        box.addView(buildMediaView(exercise, dp(210), detailWeb));
        box.addView(space(8));
        box.addView(text(exerciseReviews.description(exercise, effectiveMedia(exercise)),
                13, Typeface.NORMAL, isReviewed(exercise) ? GREEN : AMBER));
        String reviewSource = exerciseReviews.source(exercise);
        if (isWebUrl(reviewSource)) box.addView(externalLinkText("查看复核参考资料", reviewSource, 12));
        box.addView(button("复核这个动作", GREEN_SOFT, GREEN, v -> {
            dialogRef[0].dismiss(); showExerciseReview(exercise);
        }), fullButton());
        String detailMedia = effectiveMedia(exercise);
        if (isWebUrl(detailMedia) && !isImageUrl(detailMedia)) {
            box.addView(button("▶ 在浏览器打开示范", BLUE, Color.WHITE, v -> openExternal(detailMedia)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
            box.addView(space(8));
        }
        final Button[] favRef = new Button[1];
        boolean fav0 = favoriteIds.contains(exercise.id());
        Button fav = button(fav0 ? "♥ 已标心（点击取消）" : "♡ 标心",
                fav0 ? HEART_SOFT : Color.rgb(236, 240, 234),
                fav0 ? HEART_RED : INK,
                v -> {
                    if (favoriteIds.contains(exercise.id())) {
                        favoriteIds.remove(exercise.id());
                    } else {
                        favoriteIds.add(exercise.id());
                    }
                    saveState();
                    boolean f = favoriteIds.contains(exercise.id());
                    favRef[0].setText(f ? "♥ 已标心（点击取消）" : "♡ 标心");
                    restyleButton(favRef[0], f ? HEART_SOFT : Color.rgb(236, 240, 234), f ? HEART_RED : INK);
                });
        favRef[0] = fav;
        box.addView(fav, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        box.addView(space(8));
        box.addView(button("删除动作", Color.rgb(248, 235, 232), CORAL,
                v -> confirmDeleteExercise(exercise, dialogRef[0])),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(42)));
        box.addView(space(8));
        box.addView(text(join(exercise.targetRegions()) + " · " + join(exercise.movementPatterns()), 14, Typeface.BOLD, BLUE));
        box.addView(text("器械：" + equipmentLabel(exercise), 14, Typeface.NORMAL, INK));
        if (!exercise.primaryMuscles().isEmpty()) {
            box.addView(text("目标肌群：" + join(exercise.primaryMuscles()), 14, Typeface.NORMAL, INK));
        }
        if (!exercise.secondaryMuscles().isEmpty()) {
            box.addView(text("辅助肌群：" + join(exercise.secondaryMuscles()), 14, Typeface.NORMAL, MUTED));
        }
        box.addView(text("证据：" + effectiveStatus(exercise).label(), 14, Typeface.NORMAL, INK));
        if (exercise.source().length() > 0) {
            box.addView(text("来源：" + exercise.source(), 12, Typeface.NORMAL, MUTED));
        }
        box.addView(section("动作要点"));
        addNumberedSteps(box, exercise.instructions());
        if (!exercise.commonMistakes().isEmpty()) {
            box.addView(section("常见错误"));
            for (String mistake : exercise.commonMistakes()) {
                box.addView(text("· " + mistake, 14, Typeface.NORMAL, MUTED));
            }
        }
        if (!exercise.substitutions().isEmpty()) {
            box.addView(section("替代动作"));
            box.addView(text(join(exercise.substitutions()), 14, Typeface.NORMAL, MUTED));
        }

        if (exercise.evidenceStatus() == EvidenceStatus.USER_UNVERIFIED) {
            box.addView(space(12));
            box.addView(text("个人动作完成四项复核后可进入自动推荐；旧版验证标记不等于示范已复核。", 13, Typeface.NORMAL, MUTED));
        } else if (exercise.evidenceStatus() == EvidenceStatus.DEFAULT_LIBRARY) {
            box.addView(space(12));
            box.addView(text("这是默认动作库资料。中文步骤、器械和肌群已完成结构化校验；"
                    + "但不代表医疗或专业教练背书。", 13, Typeface.NORMAL, MUTED));
        }

        ScrollView scroll = new ScrollView(this);
        scroll.addView(box);
        AlertDialog.Builder builder = new AlertDialog.Builder(this)
                .setTitle(exercise.name())
                .setView(scroll)
                .setPositiveButton("关闭", null)
                .setNeutralButton("编辑", (dialog, which) -> editExercise(exercise));
        AlertDialog dialog = builder.create();
        dialogRef[0] = dialog;
        dialog.setOnDismissListener(d -> {
            if (detailWeb[0] != null) {
                detailWeb[0].destroy();
            }
        });
        dialog.show();
    }

    private Set<String> reviewedIdsForRecommendation() {
        Set<String> ids = new LinkedHashSet<>();
        for (Exercise e : allExercises()) if (isReviewed(e)) ids.add(e.id());
        return ids;
    }

    private RecommendationEngine engine() {
        List<Exercise> reviewed = new ArrayList<>();
        for (Exercise e : allExercises()) if (isReviewed(e)) reviewed.add(e);
        return new RecommendationEngine(reviewed);
    }

    private boolean isReviewed(Exercise exercise) {
        return exerciseReviews != null && exerciseReviews.reviewed(exercise, effectiveMedia(exercise));
    }

    private String reviewLabel(Exercise exercise) { return isReviewed(exercise) ? "已复核" : "未复核"; }

    private List<Exercise> trainingExercises() {
        List<Exercise> result = new ArrayList<>();
        for (Exercise e : allExercises()) if (!reviewedOnly || isReviewed(e)) result.add(e);
        return result;
    }

    private boolean matchesReviewFilter(Exercise e) {
        if ("已复核".equals(libraryReviewFilter)) return isReviewed(e);
        if ("未复核".equals(libraryReviewFilter)) return !isReviewed(e);
        if (!"全部状态".equals(libraryReviewFilter) && isReviewed(e)) return false;
        String description = exerciseReviews.description(e, effectiveMedia(e));
        if ("待补图".equals(libraryReviewFilter)) return !hasEffectiveMedia(e)
                || (isLocalUri(effectiveMedia(e)) && !canReadLocalMedia(effectiveMedia(e))) || description.contains("待补图");
        if ("待修图".equals(libraryReviewFilter)) return !isReviewed(e) && description.contains("待修图");
        if ("待核逻辑".equals(libraryReviewFilter)) return !isReviewed(e) && !description.contains("待修图")
                && !description.contains("待补图");
        return true;
    }

    private Button reviewScopeButton(Runnable refresh) {
        Button label = button("训练选材：仅已复核", GREEN_SOFT, GREEN, v ->
                Toast.makeText(this, "推荐只使用资料与示范均已复核的动作", Toast.LENGTH_SHORT).show());
        return label;
    }

    private boolean checkRequiredEquipmentSelection(List<WorkoutItem> items) {
        LinkedHashSet<String> missing = new LinkedHashSet<>();
        for (WorkoutItem item : items) for (String required : item.exercise().requiredEquipment())
            if (!equipment.contains(required)) missing.add(required);
        if (missing.isEmpty()) return true;
        new AlertDialog.Builder(this).setTitle("还缺少必需器械")
                .setMessage("这套训练还需要：" + join(new ArrayList<>(missing))
                        + "。请在设置中确认可用器械，或替换相应动作。")
                .setPositiveButton("知道了", null).show();
        return false;
    }

    private boolean checkReviewedSelection(List<WorkoutItem> items) {
        List<String> conflicts = new ArrayList<>();
        for (WorkoutItem item : items) if (!isReviewed(item.exercise()) && !conflicts.contains(item.exercise().name()))
            conflicts.add(item.exercise().name());
        if (conflicts.isEmpty()) return true;
        new AlertDialog.Builder(this).setTitle("这套训练含未复核动作")
                .setMessage("当前选择了仅已复核：\n" + join(conflicts)
                        + "\n请替换或复核这些动作，再开始训练。")
                .setPositiveButton("知道了", null).show();
        return false;
    }

    private void showExerciseReview(Exercise exercise) {
        LinearLayout box = new LinearLayout(this); box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(16), 0, dp(16), 0);
        box.addView(text("逐项看过再勾选。已复核表示资料与示范已核对，具体强度仍由训练设置决定。",
                13, Typeface.NORMAL, MUTED));
        String[] labels = {"名称、器械和目标肌群一致", "文字步骤与动作逻辑一致", "示范姿势、支撑点和顺序正确", "完整看过播放，无明显重影或错图"};
        List<CheckBox> checks = new ArrayList<>();
        for (String label : labels) { CheckBox c = new CheckBox(this); c.setText(label); box.addView(c); checks.add(c); }
        EditText note = new EditText(this); note.setHint("复核备注或发现的问题（可选）"); box.addView(note);
        AlertDialog dialog = new AlertDialog.Builder(this).setTitle("复核 · " + exercise.name()).setView(box)
                .setPositiveButton("标为已复核", null).setNegativeButton("返回动作", (d,w) -> showExerciseDetail(exercise))
                .setNeutralButton("标为未复核", (d,w) -> {
                    String[] reasons = {"待核逻辑", "待补图", "待修图 · 重影或姿势异常"};
                    new AlertDialog.Builder(this).setTitle("记录待办原因").setItems(reasons, (d2, index) ->
                            saveExerciseReview(exercise, false, reasons[index] + " " + note.getText())).show();
                }).create();
        dialog.setOnShowListener(d -> {
            Button complete = dialog.getButton(AlertDialog.BUTTON_POSITIVE); complete.setEnabled(false);
            for (CheckBox c : checks) c.setOnCheckedChangeListener((b, checked) ->
                    complete.setEnabled(checks.stream().allMatch(CheckBox::isChecked)));
            complete.setOnClickListener(v -> {
                if (saveExerciseReview(exercise, true, "四项已核对；" + note.getText())) dialog.dismiss();
            });
        }); dialog.show();
    }

    private boolean saveExerciseReview(Exercise exercise, boolean approved, String note) {
        try {
            exerciseReviews.set(exercise, effectiveMedia(exercise), approved, note);
            planGeneration++;
            if (approved && exercise.evidenceStatus() == EvidenceStatus.USER_UNVERIFIED) verifiedIds.add(exercise.id());
            if (!approved) verifiedIds.remove(exercise.id());
            saveState();
            if ("library".equals(currentTab)) renderLibrary(libraryFilter);
            Toast.makeText(this, approved ? "已标记为已复核" : "已标记为未复核", Toast.LENGTH_SHORT).show();
            return true;
        } catch (Exception error) { Toast.makeText(this, error.getMessage(), Toast.LENGTH_LONG).show(); return false; }
    }

    private void loadState() {
        SharedPreferences prefs = getSharedPreferences("fitness_state", MODE_PRIVATE);
        reviewedOnly = true;
        quickMinutes = prefs.getInt("quickMinutes", 8);
        if (quickMinutes != 8 && quickMinutes != 15 && quickMinutes != 25) quickMinutes = 8;
        defaultIntensity = parseIntensity(prefs.getString("defaultIntensityV2", prefs.getString("intensity", "MEDIUM")));
        String quickOverride = prefs.getString("quickIntensityOverrideV2", "");
        if (!prefs.contains("quickIntensityOverrideV2") && prefs.contains("quickGentle")
                && !prefs.getBoolean("quickGentle", true)) quickOverride = "MEDIUM";
        String customOverride = prefs.getString("customIntensityOverrideV2", "");
        quickIntensityOverride = quickOverride.isEmpty() ? null : parseIntensity(quickOverride);
        customIntensityOverride = customOverride.isEmpty() ? null : parseIntensity(customOverride);
        // Old false meant the user switched away from the old gentle starting mode.
        // Old true is ambiguous, so follows the saved default; new overrides are explicit.
        quickGentle = (quickIntensityOverride == null ? defaultIntensity : quickIntensityOverride) == Intensity.LOW;
        selectedIntensity = customIntensityOverride == null ? defaultIntensity : customIntensityOverride;
        selectedDurationMinutes = parseDurationMinutes(prefs.getInt("durationMinutes", selectedDurationMinutes));
        shoulderPain = parseSeverity(prefs.getString("shoulderPain", ""));
        lowerBackPain = parseSeverity(prefs.getString("lowerBackPain", ""));
        kneePain = parseSeverity(prefs.getString("kneePain", ""));
        paceFactor = prefs.getFloat("paceFactor", 1.0f);
        programUseAi = prefs.getBoolean("programUseAi", true);
        voiceEnabled = prefs.getBoolean("voiceEnabled", true);
        voiceCues.setEnabled(voiceEnabled);
        aiEnabled = prefs.getBoolean("aiEnabled", false);
        aiApiKey = prefs.getString("aiApiKey", "");
        aiModel = GeminiModelName.normalize(prefs.getString("aiModel", GeminiModelName.DEFAULT_MODEL));
        aiSearchApiKey = prefs.getString("aiSearchApiKey", "");
        String savedSearchModel = prefs.getString("aiSearchModel", "").trim();
        aiSearchProvider = prefs.getString("aiSearchProvider", "").trim();
        if (aiSearchProvider.length() == 0) {
            aiSearchProvider = savedSearchModel.startsWith("groq/") || aiSearchApiKey.startsWith("gsk_")
                    ? SEARCH_PROVIDER_GROQ : SEARCH_PROVIDER_GEMINI;
        }
        if (isGroqSearchProvider()) {
            aiSearchEndpoint = GroqEndpoint.normalize(prefs.getString(
                    "aiSearchEndpoint", GroqEndpoint.DEFAULT_ENDPOINT));
            aiSearchModel = savedSearchModel.length() == 0 ? GroqEndpoint.DEFAULT_MODEL : savedSearchModel;
        } else {
            aiSearchEndpoint = "";
            aiSearchModel = savedSearchModel.length() == 0
                    ? GeminiModelName.DEFAULT_MODEL : GeminiModelName.normalize(savedSearchModel);
        }
        if ("gemini-2.0-flash".equals(aiModel)) {
            aiModel = GeminiModelName.DEFAULT_MODEL;
        }
        String savedEquipment = prefs.getString("equipment", null);
        if (savedEquipment != null) {
            equipment.clear();
            decodeSet(savedEquipment, equipment);
        }
        decodeSet(prefs.getString("favorites", ""), favoriteIds);
        decodeSet(prefs.getString("verified", ""), verifiedIds);
        decodeSet(prefs.getString("deletedExercises", ""), deletedExerciseIds);
        decodeSet(prefs.getString("deletedCategories", ""), deletedCategories);
        loadMediaOverrides(prefs.getString("mediaOverrides", "{}"));
        loadRecentRecommendationIds(prefs.getString("recentRecommendationsV1", "[]"));
        loadRecords(prefs.getString("records", "[]"));
        loadCustomExercises(prefs.getString("customExercises", "[]"));
        loadPendingShares(prefs.getString("pendingShares", "[]"));
        loadRecipes(prefs.getString("recipes", "[]"));
        loadAssessment(prefs.getString("assessment", ""));
        loadProgram(prefs.getString("program", ""));
        loadNutritionProfile(prefs.getString("nutritionProfile", ""));
        loadFoodLogs(prefs.getString("foodLogs", "{}"));
    }

    private void persistWorkoutDraft() {
        getSharedPreferences("fitness_state", MODE_PRIVATE).edit()
                .putString("workoutDraft", workoutDraftJson()).apply();
        lastCheckpointRealtime = SystemClock.elapsedRealtime();
    }

    private String workoutDraftJson() {
        if (currentPlan == null || activeItems.isEmpty()) return "";
        try {
            long now = SystemClock.elapsedRealtime();
            JSONObject draft = new JSONObject();
            draft.put("version", 1);
            draft.put("title", currentPlan.title());
            draft.put("intensity", currentPlan.intensity().name());
            draft.put("reason", currentPlan.recommendationReason());
            draft.put("safety", currentPlan.safetyMessage());
            draft.put("limited", currentPlan.isSafetyLimited());
            draft.put("notes", new JSONArray(currentPlan.avoidanceNotes()));
            draft.put("ai", currentPlanFromAi);
            draft.put("programKey", pendingProgramKey);
            draft.put("budget", planBudgetMinutes);
            JSONArray items = new JSONArray();
            for (WorkoutItem item : activeItems) {
                Prescription p = item.prescription();
                JSONObject entry = new JSONObject();
                entry.put("id", item.exercise().id());
                entry.put("sets", p.sets());
                entry.put("reps", p.reps());
                entry.put("rpe", p.rpe());
                entry.put("rest", p.restSeconds());
                entry.put("kind", p.kind().name());
                entry.put("hold", p.holdSeconds());
                entry.put("perSide", p.perSide());
                entry.put("tempo", p.secondsPerRep());
                entry.put("reason", item.reason());
                entry.put("restAfter", item.restAfterSeconds());
                entry.put("weight", item.weight());
                items.put(entry);
            }
            draft.put("items", items);
            draft.put("active", inSession);
            if (inSession) {
                draft.put("index", sessionIndex);
                draft.put("set", sessionSetIndex);
                draft.put("phase", sessionPhase.name());
                draft.put("started", sessionStartEpochMillis);
                draft.put("elapsed", workoutClock.elapsed(now));
                draft.put("paused", workoutClock.isPaused());
                draft.put("phaseStart", workoutClock.phaseStart());
                draft.put("phaseDuration", workoutClock.phaseDuration());
                draft.put("exerciseStart", exerciseStartedActiveMillis);
                draft.put("running", exerciseRunning);
                draft.put("hadPause", sessionHadPause);
                draft.put("switched", switchSideSpoken);
                draft.put("results", new JSONArray(sessionResults));
                draft.put("stats", new JSONArray(sessionStats));
            }
            return draft.toString();
        } catch (org.json.JSONException error) {
            throw new IllegalStateException("Cannot serialize workout progress", error);
        }
    }

    private List<String> draftStrings(JSONObject object, String key) {
        List<String> values = new ArrayList<String>();
        JSONArray array = object.optJSONArray(key);
        if (array != null) for (int i = 0; i < array.length(); i++) values.add(array.optString(i));
        return values;
    }

    private void restoreWorkoutDraft() {
        SharedPreferences prefs = getSharedPreferences("fitness_state", MODE_PRIVATE);
        String raw = prefs.getString("workoutDraft", "");
        if (raw.isEmpty()) return;
        try {
            JSONObject d = new JSONObject(raw);
            if (d.getInt("version") != 1) throw new IllegalArgumentException("Unknown draft version");
            JSONArray entries = d.getJSONArray("items");
            List<WorkoutItem> items = new ArrayList<WorkoutItem>();
            for (int i = 0; i < entries.length(); i++) {
                JSONObject entry = entries.getJSONObject(i);
                Exercise exercise = exerciseById(entry.getString("id"));
                if (exercise == null) throw new IllegalArgumentException("Exercise no longer available");
                int sets = entry.getInt("sets");
                if (sets < 1 || sets > 100) throw new IllegalArgumentException("Invalid sets");
                Prescription p = "HOLD".equals(entry.getString("kind"))
                        ? Prescription.hold(sets, entry.getInt("hold"), entry.getString("rpe"),
                                entry.getInt("rest"), entry.getBoolean("perSide"))
                        : new Prescription(sets, entry.getString("reps"), entry.getString("rpe"), entry.getInt("rest"))
                                .withPerSide(entry.getBoolean("perSide"));
                p = p.withSecondsPerRep(entry.getDouble("tempo"));
                items.add(new WorkoutItem(exercise, p, favoriteIds.contains(exercise.id()), entry.optString("reason"), entry.optInt("restAfter"), entry.optString("weight")));
            }
            if (items.isEmpty()) throw new IllegalArgumentException("Empty workout");
            boolean active = d.optBoolean("active");
            if (!active && items.stream().anyMatch(item -> !isReviewed(item.exercise()))) {
                prefs.edit().putString("unreviewedWorkoutDraft", raw).remove("workoutDraft").apply();
                Toast.makeText(this, "旧课程含未复核动作，请重新安排这一练", Toast.LENGTH_LONG).show();
                return;
            }
            int index = d.optInt("index");
            int set = d.optInt("set");
            if (active && (index < 0 || index >= items.size() || set < 0 || set >= items.get(index).prescription().sets()))
                throw new IllegalArgumentException("Invalid progress");
            SessionPhase phase = active ? SessionPhase.valueOf(d.getString("phase")) : SessionPhase.PREPARE;
            if (active) {
                // A completed record and its draft are written together. This also handles legacy interrupted saves.
                for (SessionRecord r : trainingRecords) {
                    if (r.startEpochMillis > 0 && r.startEpochMillis == d.getLong("started")) {
                        prefs.edit().remove("workoutDraft").apply();
                        return;
                    }
                }
            }
            currentPlan = new WorkoutPlan(d.getString("title"), parseIntensity(d.getString("intensity")),
                    timeModel().sessionMinutes(items), items, d.optString("reason"), draftStrings(d, "notes"),
                    d.optString("safety"), d.optBoolean("limited"));
            activeItems.addAll(items);
            currentPlanFromAi = d.optBoolean("ai");
            pendingProgramKey = d.optString("programKey");
            planBudgetMinutes = d.optInt("budget");
            inSession = active;
            sessionIndex = index;
            sessionSetIndex = set;
            sessionPhase = phase;
            if (active) {
                sessionStartEpochMillis = d.getLong("started");
                workoutClock.restore(d.getLong("elapsed"), d.getLong("phaseStart"), d.getLong("phaseDuration"));
                exerciseStartedActiveMillis = d.optLong("exerciseStart");
                exerciseRunning = d.optBoolean("running");
                sessionHadPause = true;
                switchSideSpoken = d.optBoolean("switched");
                inRest = phase == SessionPhase.REST;
                sessionResults.addAll(draftStrings(d, "results"));
                sessionStats.addAll(draftStrings(d, "stats"));
            }
        } catch (Exception error) {
            // Keep the original snapshot for recovery instead of silently deleting incompatible progress.
            prefs.edit().putString("unreadableWorkoutDraft", raw).remove("workoutDraft").apply();
            currentPlan = null;
            activeItems.clear();
            inSession = false;
            pendingProgramKey = "";
            Toast.makeText(this, "上次课程暂时无法恢复，原始进度已保留；历史记录不受影响。", Toast.LENGTH_LONG).show();
        }
    }

    @Override
    public void onBackPressed() {
        handleBackNavigation();
    }

    private void handleBackNavigation() {
        if ("routine_editor".equals(trainingPage)) { leaveRoutineEditor(); return; }
        if (inSession && sessionVisible) {
            pauseWorkout();
            renderTraining();
        } else if (!"training".equals(currentTab) || !"home".equals(trainingPage)) {
            renderTraining();
        } else {
            pauseWorkout();
            moveTaskToBack(true);
        }
    }

    private void saveState() {
        SharedPreferences.Editor editor = getSharedPreferences("fitness_state", MODE_PRIVATE).edit();
        editor.putBoolean("reviewedOnlyV1", reviewedOnly);
        if (exerciseReviews != null) editor.putString("exerciseReviewsV1", exerciseReviews.save());
        editor.putInt("quickMinutes", quickMinutes);
        editor.putBoolean("quickGentle", quickGentle);
        editor.putString("workoutDraft", workoutDraftJson());
        editor.putString("intensity", defaultIntensity.name());
        editor.putString("defaultIntensityV2", defaultIntensity.name());
        editor.putString("quickIntensityOverrideV2", quickIntensityOverride == null ? "" : quickIntensityOverride.name());
        editor.putString("customIntensityOverrideV2", customIntensityOverride == null ? "" : customIntensityOverride.name());
        editor.putInt("durationMinutes", selectedDurationMinutes);
        editor.putString("shoulderPain", shoulderPain == null ? "" : shoulderPain.name());
        editor.putString("lowerBackPain", lowerBackPain == null ? "" : lowerBackPain.name());
        editor.putString("kneePain", kneePain == null ? "" : kneePain.name());
        editor.remove("includeUnverified");
        editor.putFloat("paceFactor", (float) paceFactor);
        editor.putBoolean("programUseAi", programUseAi);
        editor.putBoolean("voiceEnabled", voiceEnabled);
        editor.putBoolean("aiEnabled", aiEnabled);
        editor.putString("aiApiKey", aiApiKey);
        editor.putString("aiModel", aiModel);
        editor.putString("aiSearchApiKey", aiSearchApiKey);
        editor.putString("aiSearchProvider", aiSearchProvider);
        editor.putString("aiSearchEndpoint", aiSearchEndpoint);
        editor.putString("aiSearchModel", aiSearchModel);
        editor.putString("equipment", encodeSet(equipment));
        editor.putString("favorites", encodeSet(favoriteIds));
        editor.putString("verified", encodeSet(verifiedIds));
        editor.putString("deletedExercises", encodeSet(deletedExerciseIds));
        editor.putString("deletedCategories", encodeSet(deletedCategories));
        editor.putString("mediaOverrides", mediaOverridesJson().toString());
        editor.putString("recentRecommendationsV1", new JSONArray(recentRecommendationIds).toString());
        editor.putString("records", recordsJson().toString());
        editor.putString("customExercises", customExercisesJson().toString());
        editor.putString("pendingShares", pendingSharesJson().toString());
        editor.putString("recipes", recipesJson().toString());
        editor.putString("assessment", assessmentJson());
        editor.putString("program", programJson());
        editor.putString("nutritionProfile", nutritionProfileJson());
        editor.putString("foodLogs", foodLogsJson());
        editor.apply();
    }

    // ------------------------------------------------------------------ //
    // 周期计划 / 评估 / 营养 —— 持久化
    // ------------------------------------------------------------------ //

    private String assessmentJson() {
        if (assessment == null) {
            return "";
        }
        try {
            JSONObject object = new JSONObject();
            object.put("version", 2);
            object.put("level", assessment.level().name());
            object.put("cap", assessment.intensityCap().name());
            object.put("clearance", assessment.medicalClearanceAdvised());
            object.put("date", assessmentDate);
            JSONArray notes = new JSONArray();
            for (String note : assessment.notes()) {
                notes.put(note);
            }
            object.put("notes", notes);
            if (assessmentInput != null) {
                JSONObject input = new JSONObject();
                input.put("heartCondition", assessmentInput.heartCondition());
                input.put("chestPainActivity", assessmentInput.chestPainActivity());
                input.put("chestPainRest", assessmentInput.chestPainRest());
                input.put("dizziness", assessmentInput.dizziness());
                input.put("boneJointProblem", assessmentInput.boneJointProblem());
                input.put("bloodPressureMeds", assessmentInput.bloodPressureMeds());
                input.put("otherReason", assessmentInput.otherReason());
                input.put("trainingMonths", assessmentInput.trainingMonths());
                input.put("weeklySessions", assessmentInput.weeklySessions());
                input.put("pushupMax", assessmentInput.pushupMax());
                input.put("plankSeconds", assessmentInput.plankSeconds());
                input.put("squatCount60s", assessmentInput.squatCount60s());
                object.put("input", input);
            }
            return object.toString();
        } catch (Exception broken) {
            return "";
        }
    }

    private void loadAssessment(String raw) {
        assessment = null;
        assessmentInput = null;
        assessmentDate = "";
        if (raw == null || raw.length() == 0) {
            return;
        }
        try {
            JSONObject object = new JSONObject(raw);
            List<String> notes = new ArrayList<String>();
            JSONArray noteArray = object.optJSONArray("notes");
            if (noteArray != null) {
                for (int i = 0; i < noteArray.length(); i++) {
                    notes.add(noteArray.optString(i));
                }
            }
            assessment = new AssessmentResult(
                    TrainingLevel.parse(object.optString("level"), TrainingLevel.BEGINNER),
                    parseIntensity(object.optString("cap", Intensity.MEDIUM.name())),
                    object.optBoolean("clearance", false),
                    notes,
                    Arrays.asList(GuidelineRefs.PARQ, GuidelineRefs.LEVEL_NOTE));
            assessmentDate = object.optString("date", "");
            JSONObject input = object.optJSONObject("input");
            if (input != null) {
                AssessmentInput.Builder builder = new AssessmentInput.Builder()
                        .safetyFlags(input.optBoolean("heartCondition"),
                                input.optBoolean("chestPainActivity"),
                                input.optBoolean("chestPainRest"),
                                input.optBoolean("dizziness"),
                                input.optBoolean("boneJointProblem"),
                                input.optBoolean("bloodPressureMeds"),
                                input.optBoolean("otherReason"))
                        .history(input.optInt("trainingMonths", 0), input.optInt("weeklySessions", 0));
                int pushup = input.optInt("pushupMax", -1);
                int plank = input.optInt("plankSeconds", -1);
                int squat = input.optInt("squatCount60s", -1);
                if (pushup >= 0) builder.pushupMax(pushup);
                if (plank >= 0) builder.plankSeconds(plank);
                if (squat >= 0) builder.squatCount60s(squat);
                assessmentInput = builder.build();
            }
        } catch (Exception broken) {
            assessment = null;
            assessmentInput = null;
        }
    }

    private String programJson() {
        if (program == null) {
            return "";
        }
        try {
            JSONObject object = new JSONObject();
            object.put("goal", program.goal().name());
            object.put("level", program.level().name());
            object.put("days", program.daysPerWeek());
            JSONArray weekdays = new JSONArray();
            for (Integer weekday : programWeekdays) {
                weekdays.put(weekday.intValue());
            }
            object.put("weekdays", weekdays);
            object.put("schedule", scheduleJson());
            return object.toString();
        } catch (Exception broken) {
            return "";
        }
    }

    private JSONArray scheduleJson() {
        JSONArray array = new JSONArray();
        if (schedule == null) {
            return array;
        }
        for (ScheduledSession session : schedule.sessions()) {
            try {
                JSONObject object = new JSONObject();
                object.put("week", session.week());
                object.put("day", session.dayIndex());
                object.put("date", session.epochDay());
                object.put("focus", session.focus().name());
                object.put("status", session.status().name());
                object.put("repeat", session.isRepeatWeek());
                JSONArray ids = new JSONArray();
                for (String id : session.exerciseIds()) {
                    ids.put(id);
                }
                object.put("ids", ids);
                JSONArray slots = new JSONArray();
                for (String slot : session.slotKeys()) {
                    slots.put(slot);
                }
                object.put("slots", slots);
                array.put(object);
            } catch (Exception ignored) {
                // Skip malformed sessions instead of losing the whole calendar.
            }
        }
        return array;
    }

    private void loadProgram(String raw) {
        program = null;
        schedule = null;
        programWeekdays.clear();
        if (raw == null || raw.length() == 0) {
            return;
        }
        try {
            JSONObject object = new JSONObject(raw);
            PlanGoal goal = PlanGoal.parse(object.optString("goal"), PlanGoal.GENERAL_FITNESS);
            TrainingLevel level = TrainingLevel.parse(object.optString("level"), TrainingLevel.BEGINNER);
            int days = Math.max(2, Math.min(5, object.optInt("days", 3)));
            program = new ProgramBuilder().build(goal, level, days, assessmentCap());
            JSONArray weekdays = object.optJSONArray("weekdays");
            if (weekdays != null) {
                for (int i = 0; i < weekdays.length(); i++) {
                    programWeekdays.add(weekdays.optInt(i, 1));
                }
            }
            if (programWeekdays.isEmpty()) {
                programWeekdays.addAll(ProgramSchedule.defaultWeekdays(days));
            }
            schedule = parseSchedule(object.optJSONArray("schedule"));
            if (schedule == null || schedule.isEmpty()) {
                // 老版本没有日历（只有 "周:日" 计数）。按今天重排，并把已完成的次数补回去。
                schedule = migrateLegacySchedule(object.optJSONArray("done"));
            }
        } catch (Exception broken) {
            program = null;
            schedule = null;
        }
    }

    private ProgramSchedule parseSchedule(JSONArray array) {
        if (array == null || array.length() == 0) {
            return null;
        }
        List<ScheduledSession> sessions = new ArrayList<ScheduledSession>();
        for (int i = 0; i < array.length(); i++) {
            JSONObject object = array.optJSONObject(i);
            if (object == null) {
                continue;
            }
            List<String> ids = new ArrayList<String>();
            JSONArray rawIds = object.optJSONArray("ids");
            if (rawIds != null) {
                for (int j = 0; j < rawIds.length(); j++) {
                    ids.add(rawIds.optString(j));
                }
            }
            List<String> slots = new ArrayList<String>();
            JSONArray rawSlots = object.optJSONArray("slots");
            if (rawSlots != null) {
                for (int j = 0; j < rawSlots.length(); j++) {
                    slots.add(rawSlots.optString(j));
                }
            }
            sessions.add(new ScheduledSession(
                    object.optInt("week", 1),
                    object.optInt("day", 0),
                    object.optLong("date", 0L),
                    ProgramFocus.parse(object.optString("focus"), ProgramFocus.FULL_A),
                    ids, slots,
                    parseSessionStatus(object.optString("status")),
                    object.optBoolean("repeat", false)));
        }
        return sessions.isEmpty() ? null : new ProgramSchedule(sessions);
    }

    private ScheduledSession.Status parseSessionStatus(String value) {
        for (ScheduledSession.Status status : ScheduledSession.Status.values()) {
            if (status.name().equals(value)) {
                return status;
            }
        }
        return ScheduledSession.Status.PLANNED;
    }

    /** 老计划升级：日期信息本来就不存在，只能按今天重排，保留已完成的次数。 */
    private ProgramSchedule migrateLegacySchedule(JSONArray done) {
        ProgramSchedule built = buildSchedule(program, todayEpochDay(), programWeekdays);
        int completed = done == null ? 0 : done.length();
        for (int i = 0; i < completed && i < built.sessions().size(); i++) {
            built = built.withSession(
                    built.sessions().get(i).withStatus(ScheduledSession.Status.DONE));
        }
        return built;
    }

    private Intensity assessmentCap() {
        return assessment == null ? Intensity.HIGH : assessment.intensityCap();
    }

    private String nutritionProfileJson() {
        if (nutritionProfile == null) {
            return "";
        }
        try {
            JSONObject object = new JSONObject();
            object.put("male", nutritionProfile.male());
            object.put("age", nutritionProfile.age());
            object.put("height", nutritionProfile.heightCm());
            object.put("weight", nutritionProfile.weightKg());
            object.put("activity", nutritionProfile.activity().name());
            object.put("goal", nutritionProfile.goal().name());
            return object.toString();
        } catch (Exception broken) {
            return "";
        }
    }

    private void loadNutritionProfile(String raw) {
        nutritionProfile = null;
        if (raw == null || raw.length() == 0) {
            return;
        }
        try {
            JSONObject object = new JSONObject(raw);
            nutritionProfile = new NutritionProfile(
                    object.optBoolean("male", true),
                    object.optInt("age", 30),
                    object.optDouble("height", 170),
                    object.optDouble("weight", 65),
                    ActivityLevel.parse(object.optString("activity"), ActivityLevel.LIGHT),
                    PlanGoal.parse(object.optString("goal"), PlanGoal.GENERAL_FITNESS));
        } catch (Exception broken) {
            nutritionProfile = null;
        }
    }

    private void rebuildNutritionDerived() {
        if (nutritionProfile == null) {
            energyPlan = null;
            pagodaTargets = null;
            return;
        }
        energyPlan = new NutritionPlanner().plan(nutritionProfile);
        pagodaTargets = PagodaTargets.forEnergy(energyPlan.targetKcal());
    }

    private String foodLogsJson() {
        try {
            JSONObject root = new JSONObject();
            for (Map.Entry<String, DayFoodLog> entry : foodLogs.entrySet()) {
                DayFoodLog log = entry.getValue();
                JSONObject day = new JSONObject();
                JSONObject groups = new JSONObject();
                for (FoodGroup group : FoodGroup.values()) {
                    if (log.grams(group) > 0) {
                        groups.put(group.name(), log.grams(group));
                    }
                }
                day.put("groups", groups);
                day.put("kcal", log.kcal());
                day.put("protein", log.protein());
                day.put("fiber", log.fiber());
                day.put("water", log.waterMl());
                JSONArray eaten = new JSONArray();
                for (String id : log.recipeIds()) {
                    eaten.put(id);
                }
                day.put("recipes", eaten);
                JSONArray entries = new JSONArray();
                for (FoodLogEntry logged : log.entries()) {
                    JSONObject item = new JSONObject();
                    item.put("label", logged.label());
                    item.put("kcal", logged.kcal());
                    item.put("protein", logged.protein());
                    item.put("fiber", logged.fiber());
                    item.put("recipe", logged.recipeId());
                    item.put("at", logged.epochMillis());
                    JSONObject itemGrams = new JSONObject();
                    for (Map.Entry<FoodGroup, Integer> part : logged.grams().entrySet()) {
                        itemGrams.put(part.getKey().name(), part.getValue());
                    }
                    item.put("grams", itemGrams);
                    entries.put(item);
                }
                day.put("entries", entries);
                root.put(entry.getKey(), day);
            }
            return root.toString();
        } catch (Exception broken) {
            return "{}";
        }
    }

    private void loadFoodLogs(String raw) {
        foodLogs.clear();
        try {
            JSONObject root = new JSONObject(raw == null || raw.length() == 0 ? "{}" : raw);
            java.util.Iterator<String> keys = root.keys();
            long keepAfter = System.currentTimeMillis() - 45L * 24 * 3600 * 1000;
            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA);
            while (keys.hasNext()) {
                String key = keys.next();
                try {
                    Date day = format.parse(key);
                    if (day != null && day.getTime() < keepAfter) {
                        continue;  // 只保留最近 45 天
                    }
                } catch (Exception ignored) {
                    continue;
                }
                JSONObject dayJson = root.optJSONObject(key);
                if (dayJson == null) {
                    continue;
                }
                DayFoodLog log = new DayFoodLog();
                JSONObject groups = dayJson.optJSONObject("groups");
                if (groups != null) {
                    for (FoodGroup group : FoodGroup.values()) {
                        log.setGrams(group, groups.optInt(group.name(), 0));
                    }
                }
                log.restoreTotals(dayJson.optInt("kcal", 0), dayJson.optInt("protein", 0),
                        dayJson.optInt("fiber", 0), dayJson.optInt("water", 0));
                JSONArray eaten = dayJson.optJSONArray("recipes");
                if (eaten != null) {
                    for (int i = 0; i < eaten.length(); i++) {
                        log.restoreRecipeId(eaten.optString(i));
                    }
                }
                JSONArray entries = dayJson.optJSONArray("entries");
                if (entries != null) {
                    for (int i = 0; i < entries.length(); i++) {
                        JSONObject item = entries.optJSONObject(i);
                        if (item == null) {
                            continue;
                        }
                        Map<FoodGroup, Integer> itemGrams =
                                new EnumMap<FoodGroup, Integer>(FoodGroup.class);
                        JSONObject gramsJson = item.optJSONObject("grams");
                        if (gramsJson != null) {
                            for (FoodGroup group : FoodGroup.values()) {
                                int value = gramsJson.optInt(group.name(), 0);
                                if (value > 0) {
                                    itemGrams.put(group, value);
                                }
                            }
                        }
                        log.restoreEntry(new FoodLogEntry(item.optString("label"),
                                item.optInt("kcal", 0), item.optInt("protein", 0),
                                item.optInt("fiber", 0), itemGrams, item.optString("recipe"),
                                item.optLong("at", 0L)));
                    }
                }
                foodLogs.put(key, log);
            }
        } catch (Exception broken) {
            foodLogs.clear();
        }
    }

    private JSONArray recordsJson() {
        JSONArray array = new JSONArray();
        for (SessionRecord record : trainingRecords) {
            try {
                JSONObject object = new JSONObject();
                object.put("time", record.time);
                object.put("title", record.title);
                object.put("total", record.total);
                object.put("done", record.done);
                object.put("feel", record.feel);
                object.put("pain", record.pain);
                object.put("note", record.note);
                object.put("duration", record.duration);
                object.put("epoch", record.epochMillis);
                object.put("startEpoch", record.startEpochMillis);
                object.put("timingNote", record.timingNote);
                object.put("metrics", record.metrics);
                JSONArray details = new JSONArray();
                for (WorkoutEntry entry : record.details) details.put(entry.json());
                object.put("details", details);
                if (record.hrAvg > 0) {
                    object.put("hrAvg", record.hrAvg);
                    object.put("hrMax", record.hrMax);
                    object.put("hrMin", record.hrMin);
                    object.put("hrSeries", record.hrSeries);
                    object.put("hrSamples", record.hrSamples);
                    object.put("hrCoverage", record.hrCoveragePercent);
                    object.put("hrReliable", record.hrReliable);
                    object.put("hrSource", record.hrSource);
                }
                JSONArray items = new JSONArray();
                for (String line : record.itemLines) {
                    items.put(line);
                }
                object.put("items", items);
                JSONArray stats = new JSONArray();
                for (String stat : record.itemStats) {
                    stats.put(stat);
                }
                object.put("itemStats", stats);
                array.put(object);
            } catch (Exception ignored) {
                // Skip malformed records instead of blocking app startup.
            }
        }
        return array;
    }

    private JSONObject mediaOverridesJson() {
        JSONObject object = new JSONObject();
        for (Map.Entry<String, String> entry : mediaOverrides.entrySet()) {
            try {
                object.put(entry.getKey(), entry.getValue());
            } catch (Exception ignored) {
                // Skip malformed entries instead of blocking app startup.
            }
        }
        return object;
    }

    private void loadMediaOverrides(String raw) {
        mediaOverrides.clear();
        try {
            JSONObject object = new JSONObject(raw);
            java.util.Iterator<String> keys = object.keys();
            while (keys.hasNext()) {
                String key = keys.next();
                String value = object.optString(key);
                if (value != null && value.length() > 0) {
                    mediaOverrides.put(key, value);
                }
            }
        } catch (Exception ignored) {
            mediaOverrides.clear();
        }
    }

    private void loadRecentRecommendationIds(String raw) {
        recentRecommendationIds.clear();
        try {
            JSONArray array = new JSONArray(raw);
            for (int i = 0; i < array.length() && recentRecommendationIds.size() < 24; i++) {
                String id = array.optString(i);
                if (id.length() > 0 && !recentRecommendationIds.contains(id)) {
                    recentRecommendationIds.add(id);
                }
            }
        } catch (Exception ignored) {
            recentRecommendationIds.clear();
        }
    }

    private JSONArray customExercisesJson() {
        JSONArray array = new JSONArray();
        for (Exercise exercise : customExercises) {
            JSONObject object = new JSONObject();
            try {
                object.put("id", exercise.id());
                object.put("name", exercise.name());
                JSONArray regions = new JSONArray();
                for (String region : exercise.targetRegions()) {
                    regions.put(region);
                }
                object.put("regions", regions);
                JSONArray requiredEquipment = new JSONArray();
                for (String item : exercise.equipment()) {
                    requiredEquipment.put(item);
                }
                object.put("equipment", requiredEquipment);
                StringBuilder joined = new StringBuilder();
                for (String line : exercise.instructions()) {
                    if (joined.length() > 0) {
                        joined.append("\n");
                    }
                    joined.append(line);
                }
                object.put("instruction", joined.toString());
                object.put("media", exercise.media());
                array.put(object);
            } catch (Exception ignored) {
                // Skip malformed local drafts instead of blocking app startup.
            }
        }
        return array;
    }

    private JSONArray recipesJson() {
        JSONArray array = new JSONArray();
        for (Recipe recipe : recipes) {
            try {
                JSONObject object = new JSONObject();
                object.put("id", recipe.id);
                object.put("name", recipe.name);
                object.put("sourceMedia", recipe.sourceMedia);
                object.put("sourceUrl", recipe.sourceUrl);
                object.put("note", recipe.note);
                object.put("review", recipe.review);
                object.put("rating", recipe.rating);
                object.put("createdAt", recipe.createdAt);
                object.put("builtinId", recipe.builtinId);
                object.put("kcal", recipe.kcal);
                object.put("protein", recipe.proteinG);
                object.put("fiber", recipe.fiberG);
                JSONObject groupGrams = new JSONObject();
                for (Map.Entry<FoodGroup, Integer> part : recipe.groupGrams.entrySet()) {
                    groupGrams.put(part.getKey().name(), part.getValue());
                }
                object.put("groupGrams", groupGrams);
                JSONArray tags = new JSONArray();
                for (String tag : recipe.tags) {
                    tags.put(tag);
                }
                object.put("tags", tags);
                JSONArray photos = new JSONArray();
                for (String photo : recipe.photos) {
                    photos.put(photo);
                }
                object.put("photos", photos);
                JSONArray ingredients = new JSONArray();
                for (String ingredient : recipe.ingredients) {
                    ingredients.put(ingredient);
                }
                object.put("ingredients", ingredients);
                JSONArray steps = new JSONArray();
                for (RecipeStep step : recipe.steps) {
                    JSONObject stepObject = new JSONObject();
                    stepObject.put("text", step.text);
                    stepObject.put("image", step.image);
                    steps.put(stepObject);
                }
                object.put("steps", steps);
                array.put(object);
            } catch (Exception ignored) {
                // Skip malformed recipes instead of blocking app startup.
            }
        }
        return array;
    }

    private void loadRecipes(String raw) {
        recipes.clear();
        try {
            JSONArray array = new JSONArray(raw);
            for (int i = 0; i < array.length(); i++) {
                JSONObject object = array.optJSONObject(i);
                if (object == null) {
                    continue;
                }
                recipes.add(recipeFromJson(object, i));
            }
        } catch (Exception ignored) {
            recipes.clear();
        }
    }

    private Recipe recipeFromJson(JSONObject object, int index) {
        Recipe recipe = new Recipe();
        recipe.id = object.optString("id", "recipe_" + index);
        if (recipe.id.length() == 0) {
            recipe.id = "recipe_" + index;
        }
        recipe.name = object.optString("name");
        recipe.sourceMedia = object.optString("sourceMedia");
        recipe.sourceUrl = object.optString("sourceUrl");
        recipe.note = object.optString("note");
        recipe.review = object.optString("review");
        recipe.rating = object.optInt("rating", 0);
        recipe.createdAt = object.optLong("createdAt", 0L);
        recipe.builtinId = object.optString("builtinId");
        recipe.kcal = object.optInt("kcal", 0);
        recipe.proteinG = object.optInt("protein", 0);
        recipe.fiberG = object.optInt("fiber", 0);
        JSONObject groupGrams = object.optJSONObject("groupGrams");
        if (groupGrams != null) {
            for (FoodGroup group : FoodGroup.values()) {
                int value = groupGrams.optInt(group.name(), 0);
                if (value > 0) {
                    recipe.groupGrams.put(group, value);
                }
            }
        }
        JSONArray tags = object.optJSONArray("tags");
        if (tags != null) {
            for (int j = 0; j < tags.length(); j++) {
                String tag = tags.optString(j);
                if (tag != null && tag.length() > 0) {
                    recipe.tags.add(tag);
                }
            }
        }
        JSONArray photos = object.optJSONArray("photos");
        if (photos != null) {
            for (int j = 0; j < photos.length(); j++) {
                String photo = photos.optString(j);
                if (photo != null && photo.length() > 0) {
                    recipe.photos.add(photo);
                }
            }
        }
        JSONArray ingredients = object.optJSONArray("ingredients");
        if (ingredients != null) {
            for (int j = 0; j < ingredients.length(); j++) {
                String ingredient = ingredients.optString(j);
                if (ingredient != null && ingredient.length() > 0) {
                    recipe.ingredients.add(ingredient);
                }
            }
        }
        JSONArray steps = object.optJSONArray("steps");
        if (steps != null) {
            for (int j = 0; j < steps.length(); j++) {
                JSONObject stepObject = steps.optJSONObject(j);
                if (stepObject != null) {
                    String stepText = stepObject.optString("text");
                    String stepImage = stepObject.optString("image");
                    if (stepText.length() > 0 || stepImage.length() > 0) {
                        recipe.steps.add(new RecipeStep(stepText, stepImage));
                    }
                } else {
                    String legacy = steps.optString(j);
                    if (legacy != null && legacy.length() > 0) {
                        recipe.steps.add(new RecipeStep(legacy, ""));
                    }
                }
            }
        }
        return recipe;
    }

    private JSONArray pendingSharesJson() {
        JSONArray array = new JSONArray();
        for (PendingShare share : pendingShares) {
            JSONObject object = new JSONObject();
            try {
                object.put("title", share.title);
                object.put("body", share.body);
                object.put("uri", share.uri);
                object.put("createdAt", share.createdAt);
                array.put(object);
            } catch (Exception ignored) {
                // Skip malformed share drafts instead of blocking app startup.
            }
        }
        return array;
    }

    private SessionRecord recordFromJson(JSONObject object) {
        List<String> stats = new ArrayList<String>();
        JSONArray rawStats = object.optJSONArray("itemStats");
        if (rawStats != null) {
            for (int j = 0; j < rawStats.length(); j++) {
                stats.add(rawStats.optString(j));
            }
        }
        List<String> lines = new ArrayList<String>();
        JSONArray items = object.optJSONArray("items");
        if (items != null) {
            for (int j = 0; j < items.length(); j++) {
                lines.add(items.optString(j));
            }
        }
        SessionRecord record = new SessionRecord(
                object.optString("time"),
                object.optString("title"),
                object.optInt("total"),
                object.optInt("done"),
                object.optString("feel"),
                object.optString("pain"),
                object.optString("note"),
                lines,
                object.optString("duration"),
                object.optLong("epoch", 0L),
                object.optLong("startEpoch", 0L),
                object.optInt("hrAvg", 0),
                object.optInt("hrMax", 0),
                object.optInt("hrMin", 0),
                object.optString("hrSeries", ""),
                object.optInt("hrSamples", 0),
                object.optInt("hrCoverage", 0),
                object.optBoolean("hrReliable", false),
                object.optString("hrSource", ""),
                stats);
        record.metrics = object.optJSONObject("metrics") == null ? new JSONObject() : object.optJSONObject("metrics");
        record.timingNote = object.optString("timingNote");
        JSONArray details = object.optJSONArray("details");
        if (details != null) for (int i = 0; i < details.length(); i++) {
            JSONObject entry = details.optJSONObject(i); if (entry != null) record.details.add(WorkoutEntry.from(entry));
        }
        if (record.details.isEmpty()) for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i), name = line.split(" · ", 2)[0].replaceFirst("^[✓◐○]\\s*", "");
            String id = ""; int completed = 0; boolean finished = line.startsWith("✓");
            if (i < stats.size()) { String[] fields = stats.get(i).split("\\|");
                if (fields.length >= 3) { id = fields[0]; try { completed = Integer.parseInt(fields[1]); } catch (Exception ignored) {} } }
            record.details.add(new WorkoutEntry(id, name, null, completed, finished, 75, "", line));
        }
        return record;
    }

    private void loadRecords(String raw) {
        trainingRecords.clear();
        try {
            JSONArray array = new JSONArray(raw);
            for (int i = 0; i < array.length(); i++) {
                JSONObject object = array.optJSONObject(i);
                if (object != null) {
                    trainingRecords.add(recordFromJson(object));
                } else {
                    String legacy = array.optString(i);
                    if (legacy != null && legacy.length() > 0) {
                        trainingRecords.add(SessionRecord.legacy(legacy));
                    }
                }
            }
        } catch (Exception ignored) {
            trainingRecords.clear();
        }
    }

    private void loadCustomExercises(String raw) {
        customExercises.clear();
        try {
            JSONArray array = new JSONArray(raw);
            for (int i = 0; i < array.length(); i++) {
                JSONObject object = array.optJSONObject(i);
                if (object != null) {
                    List<String> regions = new ArrayList<String>();
                    JSONArray regionArray = object.optJSONArray("regions");
                    if (regionArray != null) {
                        for (int j = 0; j < regionArray.length(); j++) {
                            String region = regionArray.optString(j);
                            if (region != null && region.length() > 0) {
                                regions.add(region);
                            }
                        }
                    } else {
                        regions.add(object.optString("region", "背"));
                    }
                    List<String> requiredEquipment = new ArrayList<String>();
                    JSONArray equipmentArray = object.optJSONArray("equipment");
                    if (equipmentArray != null) {
                        for (int j = 0; j < equipmentArray.length(); j++) {
                            String item = equipmentArray.optString(j);
                            if (item != null && item.length() > 0) requiredEquipment.add(item);
                        }
                    } else {
                        String legacyEquipment = object.optString("equipment", "自重");
                        if (legacyEquipment.length() > 0) requiredEquipment.add(legacyEquipment);
                    }
                    customExercises.add(customExercise(object.optString("id"),
                            object.optString("name"),
                            regions,
                            object.optString("instruction"),
                            object.optString("media"),
                            requiredEquipment));
                }
            }
        } catch (Exception ignored) {
            customExercises.clear();
        }
    }

    private void loadPendingShares(String raw) {
        pendingShares.clear();
        try {
            JSONArray array = new JSONArray(raw);
            for (int i = 0; i < array.length(); i++) {
                JSONObject object = array.optJSONObject(i);
                if (object != null) {
                    pendingShares.add(new PendingShare(object.optString("title"),
                            object.optString("body"),
                            object.optString("uri"),
                            object.optString("createdAt")));
                }
            }
        } catch (Exception ignored) {
            pendingShares.clear();
        }
    }

    private String encodeSet(Set<String> values) {
        StringBuilder builder = new StringBuilder();
        for (String value : values) {
            if (builder.length() > 0) {
                builder.append("|");
            }
            builder.append(value);
        }
        return builder.toString();
    }

    private void decodeSet(String raw, Set<String> target) {
        if (raw == null || raw.length() == 0) {
            return;
        }
        String[] parts = raw.split("\\|");
        for (String part : parts) {
            if (part.length() > 0) {
                target.add(part);
            }
        }
    }

    private Intensity parseIntensity(String raw) {
        try {
            return Intensity.valueOf(raw);
        } catch (Exception ignored) {
            return Intensity.MEDIUM;
        }
    }

    private int parseDurationMinutes(int raw) {
        if (raw == 0) {
            return 0;
        }
        if (raw <= 5) {
            return 5;
        }
        if (raw <= 15) {
            return 15;
        }
        if (raw <= 25) {
            return 25;
        }
        if (raw <= 40) {
            return 40;
        }
        return 55;
    }

    private String durationLabel(int minutes) {
        return minutes <= 0 ? "不限时（按动作估时）" : minutes + " 分钟";
    }

    private PainSeverity parseSeverity(String raw) {
        try {
            return raw == null || raw.length() == 0 ? null : PainSeverity.valueOf(raw);
        } catch (Exception ignored) {
            return null;
        }
    }

    private List<Exercise> allExercises() {
        List<Exercise> exercises = new ArrayList<Exercise>();
        for (Exercise exercise : seedExercises) {
            if (!deletedExerciseIds.contains(exercise.id())) {
                exercises.add(exercise);
            }
        }
        for (Exercise exercise : datasetExercises) {
            if (!deletedExerciseIds.contains(exercise.id())) {
                exercises.add(exercise);
            }
        }
        for (Exercise exercise : customExercises) {
            if (!deletedExerciseIds.contains(exercise.id())) {
                exercises.add(exercise);
            }
        }
        return exercises;
    }

    private String equipmentLabel(Exercise exercise) {
        return join(exercise.equipment()) + (exercise.requiredEquipment().isEmpty() ? ""
                : " + " + join(exercise.requiredEquipment()));
    }

    private List<String> equipmentOptions() {
        LinkedHashSet<String> options = new LinkedHashSet<String>(Arrays.asList(
                "自重", "弹力带", "哑铃", "杠铃", "固定器械", "高位下拉器", "壶铃", "TRX 悬挂带"));
        for (Exercise exercise : datasetExercises) {
            options.addAll(exercise.equipment());
            options.addAll(exercise.requiredEquipment());
        }
        return new ArrayList<String>(options);
    }

    private void loadBundledExerciseDataset() {
        datasetExercises.clear();
        datasetLoadError = "";
        try {
            datasetExercises.addAll(ExerciseDatasetLoader.load(
                    getAssets().open(ExerciseDatasetLoader.ASSET_NAME)));
        } catch (Exception error) {
            datasetExercises.clear();
            datasetLoadError = error.getMessage() == null
                    ? error.getClass().getSimpleName() : error.getMessage();
        }
    }

    private void clear() {
        stopTicker();
        trainingPage = "detail";
        sessionVisible = false;
        if (sessionChronometer != null) sessionChronometer.stop();
        if (setChronometer != null) setChronometer.stop();
        sessionChronometer = null;
        setChronometer = null;
        countdownLabel = null;
        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        content.removeAllViews();
    }

    // ------------------------------------------------------------------ //
    // 营养：目标（膳食指南 2022 + DRIs）→ 今日宝塔打卡 → 按缺口推荐食谱
    // ------------------------------------------------------------------ //

    private String todayKey() {
        return new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA).format(new Date());
    }

    private DayFoodLog todayLog() {
        String key = todayKey();
        DayFoodLog log = foodLogs.get(key);
        if (log == null) {
            log = new DayFoodLog();
            foodLogs.put(key, log);
        }
        return log;
    }

    private boolean isTrainingDayToday() {
        String prefix = new SimpleDateFormat("MM-dd", Locale.CHINA).format(new Date());
        for (SessionRecord record : trainingRecords) {
            if (record.time.startsWith(prefix)) {
                return true;
            }
        }
        return pendingProgramKey.length() > 0;
    }

    private String currentMealSlot() {
        int hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY);
        if (hour < 10) {
            return "早餐";
        }
        if (hour < 14) {
            return "午餐";
        }
        if (hour < 17) {
            return "加餐";
        }
        return "晚餐";
    }

    private BuiltinRecipe builtinRecipeById(String id) {
        for (BuiltinRecipe recipe : builtinRecipes) {
            if (recipe.id().equals(id)) {
                return recipe;
            }
        }
        return null;
    }

    private View nutritionSummaryCard() {
        LinearLayout card = card();
        if (nutritionProfile == null || energyPlan == null) {
            card.addView(section("营养目标"));
            card.addView(space(6));
            card.addView(text("按《中国居民膳食指南(2022)》和你的身体数据，算出每天该吃多少：热量、蛋白质、"
                    + "膳食纤维和宝塔各类食物的克数，之后的推荐都对着这些目标来，不再随机。",
                    14, Typeface.NORMAL, MUTED));
            card.addView(space(10));
            card.addView(button("设置身体数据，生成目标", GREEN, Color.WHITE, v -> renderNutritionSetup()),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));
            return card;
        }
        card.addView(section("每日营养目标 · " + nutritionProfile.goal().label()));
        card.addView(space(6));
        card.addView(text(energyPlan.targetKcal() + " kcal · 蛋白 " + energyPlan.proteinG()
                + "g（" + energyPlan.proteinPerKg() + "g/kg）", 18, Typeface.BOLD, INK));
        card.addView(text("脂肪 " + energyPlan.fatG() + "g · 碳水 " + energyPlan.carbG()
                + "g · 纤维 " + energyPlan.fiberMinG() + "-" + energyPlan.fiberMaxG()
                + "g · 水 " + energyPlan.waterMinMl() + "-" + energyPlan.waterMaxMl() + "ml · 盐 <5g",
                13, Typeface.NORMAL, MUTED));
        card.addView(space(4));
        card.addView(text("基础代谢 " + energyPlan.bmrKcal() + " · 日常消耗 " + energyPlan.tdeeKcal()
                + "（" + nutritionProfile.activity().label() + "）", 12, Typeface.NORMAL, MUTED));
        card.addView(space(8));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(button("依据", Color.rgb(236, 240, 234), INK, v -> {
            StringBuilder message = new StringBuilder();
            if (!energyPlan.notes().isEmpty()) {
                message.append("给你的提醒\n");
                for (String note : energyPlan.notes()) {
                    message.append("· ").append(note).append("\n");
                }
                message.append("\n目标依据\n");
            }
            for (String ref : energyPlan.refs()) {
                message.append("· ").append(ref).append("\n\n");
            }
            new AlertDialog.Builder(this)
                    .setTitle("这些目标的科学依据")
                    .setMessage(message.toString().trim())
                    .setPositiveButton("知道了", null)
                    .show();
        }), new LinearLayout.LayoutParams(0, dp(42), 1f));
        row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        row.addView(button("修改档案", BLUE, Color.WHITE, v -> renderNutritionSetup()),
                new LinearLayout.LayoutParams(0, dp(42), 1f));
        card.addView(row);
        return card;
    }

    private void renderNutritionSetup() {
        currentTab = "food";
        clear();
        content.addView(title("营养档案", "身体数据 + 目标 → 每日营养目标"));

        LinearLayout form = card();
        form.addView(section("身体数据"));
        form.addView(space(6));
        final RadioGroup sexGroup = new RadioGroup(this);
        sexGroup.setOrientation(RadioGroup.HORIZONTAL);
        String[] sexes = {"男", "女"};
        boolean male = nutritionProfile == null || nutritionProfile.male();
        for (int i = 0; i < sexes.length; i++) {
            RadioButton radio = new RadioButton(this);
            radio.setId(9300 + i);
            radio.setText(sexes[i]);
            radio.setTextColor(INK);
            if ((i == 0) == male) {
                radio.setChecked(true);
            }
            sexGroup.addView(radio);
        }
        form.addView(sexGroup);
        form.addView(space(8));
        form.addView(smallLabel("年龄"));
        final EditText ageField = numberField("如：30");
        if (nutritionProfile != null) {
            ageField.setText(String.valueOf(nutritionProfile.age()));
        }
        form.addView(ageField, matchWrap());
        form.addView(space(8));
        form.addView(smallLabel("身高（cm）"));
        final EditText heightField = numberField("如：172");
        if (nutritionProfile != null) {
            heightField.setText(String.valueOf((int) nutritionProfile.heightCm()));
        }
        form.addView(heightField, matchWrap());
        form.addView(space(8));
        form.addView(smallLabel("体重（kg）"));
        final EditText weightField = numberField("如：65");
        if (nutritionProfile != null) {
            weightField.setText(String.valueOf((int) nutritionProfile.weightKg()));
        }
        form.addView(weightField, matchWrap());
        content.addView(form);

        LinearLayout activityCard = card();
        activityCard.addView(section("日常活动水平"));
        activityCard.addView(space(6));
        final RadioGroup activityGroup = new RadioGroup(this);
        ActivityLevel[] levels = ActivityLevel.values();
        ActivityLevel currentActivity = nutritionProfile == null
                ? ActivityLevel.LIGHT : nutritionProfile.activity();
        for (int i = 0; i < levels.length; i++) {
            RadioButton radio = new RadioButton(this);
            radio.setId(9400 + i);
            radio.setText(levels[i].label() + " —— " + levels[i].description());
            radio.setTextColor(INK);
            radio.setTextSize(14);
            if (levels[i] == currentActivity) {
                radio.setChecked(true);
            }
            activityGroup.addView(radio);
        }
        activityCard.addView(activityGroup);
        content.addView(activityCard);

        LinearLayout goalCard = card();
        goalCard.addView(section("饮食目标"));
        goalCard.addView(space(6));
        final RadioGroup goalGroup = new RadioGroup(this);
        PlanGoal[] goals = PlanGoal.values();
        PlanGoal currentGoal = nutritionProfile == null
                ? (program != null ? program.goal() : PlanGoal.GENERAL_FITNESS)
                : nutritionProfile.goal();
        for (int i = 0; i < goals.length; i++) {
            RadioButton radio = new RadioButton(this);
            radio.setId(9500 + i);
            radio.setText(goals[i].label());
            radio.setTextColor(INK);
            if (goals[i] == currentGoal) {
                radio.setChecked(true);
            }
            goalGroup.addView(radio);
        }
        goalCard.addView(goalGroup);
        if (program != null) {
            goalCard.addView(space(4));
            goalCard.addView(text("建议与训练周期目标一致（当前计划：" + program.goal().label() + "）。",
                    12, Typeface.NORMAL, MUTED));
        }
        content.addView(goalCard);

        LinearLayout actions = card();
        actions.addView(button("生成营养目标", GREEN, Color.WHITE, v -> {
            boolean isMale = sexGroup.getCheckedRadioButtonId() == 9300;
            int age = parseIntField(ageField, 30);
            int height = parseIntField(heightField, 170);
            int weight = parseIntField(weightField, 65);
            int activityIndex = Math.max(0, Math.min(levels.length - 1,
                    activityGroup.getCheckedRadioButtonId() - 9400));
            int goalIndex = Math.max(0, Math.min(goals.length - 1,
                    goalGroup.getCheckedRadioButtonId() - 9500));
            nutritionProfile = new NutritionProfile(isMale, age, height, weight,
                    levels[activityIndex], goals[goalIndex]);
            rebuildNutritionDerived();
            saveState();
            Toast.makeText(this, "已生成每日营养目标", Toast.LENGTH_SHORT).show();
            renderFood();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(50)));
        actions.addView(space(8));
        actions.addView(button("返回", Color.rgb(236, 240, 234), INK, v -> renderFood()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        content.addView(actions);
        renderBottomNav();
    }

    private View todayFoodLogCard() {
        LinearLayout card = card();
        final DayFoodLog log = todayLog();

        final LinearLayout details = new LinearLayout(this);
        details.setOrientation(LinearLayout.VERTICAL);

        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout heading = new LinearLayout(this);
        heading.setOrientation(LinearLayout.VERTICAL);
        heading.addView(section("今日饮食记录"));
        heading.addView(text(foodLogOverview(log), 12, Typeface.NORMAL, MUTED));
        header.addView(heading,
                new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        final Button toggle = button(foodLogExpanded ? "收起" : "展开明细",
                Color.rgb(236, 240, 234), GREEN, v -> {
                    foodLogExpanded = !foodLogExpanded;
                    details.setVisibility(foodLogExpanded ? View.VISIBLE : View.GONE);
                    ((Button) v).setText(foodLogExpanded ? "收起" : "展开明细");
                });
        toggle.setTextSize(12);
        header.addView(toggle, new LinearLayout.LayoutParams(dp(82), dp(36)));
        header.setOnClickListener(v -> toggle.performClick());
        card.addView(header);

        if (log.kcal() > 0 || log.protein() > 0) {
            card.addView(space(7));
            card.addView(text("已记录食谱估算：" + log.kcal() + "/" + energyPlan.targetKcal()
                    + " kcal · 蛋白 " + log.protein() + "/" + energyPlan.proteinG()
                    + "g · 纤维 " + log.fiber() + "g", 13, Typeface.BOLD, BLUE));
        }
        card.addView(space(9));
        card.addView(button("＋ 记一餐（外卖 / 零食 / 估不准的）", GREEN, Color.WHITE,
                v -> renderQuickLog()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));

        details.addView(space(12));
        if (!log.entries().isEmpty()) {
            details.addView(committedEntriesBlock(log));
            details.addView(space(10));
        }
        details.addView(text("分类明细", 14, Typeface.BOLD, INK));
        details.addView(space(2));
        details.addView(text("点数字可精确输入，± 用来快速微调。",
                12, Typeface.NORMAL, MUTED));
        details.addView(space(6));
        for (final FoodGroup group : FoodGroup.values()) {
            final int eaten = log.grams(group);
            final int target = pagodaTargets.gramsFor(group);
            final boolean trackOnly = target <= 0; // 「零食·其他」等无正向目标的类别
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(0, dp(4), 0, dp(4));
            boolean enough = !trackOnly && eaten >= target;
            row.addView(text(group.label(), 14, Typeface.BOLD, enough ? GREEN : INK),
                    new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            String amountLabel = trackOnly ? eaten + "g" : eaten + "/" + target + "g";
            boolean tracked = trackOnly && eaten > 0;
            TextView amount = text(amountLabel, 13,
                    enough || tracked ? Typeface.BOLD : Typeface.NORMAL,
                    enough ? GREEN : tracked ? AMBER : MUTED);
            amount.setGravity(Gravity.CENTER);
            amount.setMinWidth(dp(72));
            amount.setMinHeight(dp(36));
            amount.setPadding(dp(8), 0, dp(8), 0);
            amount.setBackground(bg(Color.rgb(247, 249, 245), dp(9), LINE, 1));
            amount.setOnClickListener(v -> editGroupGrams(group));
            row.addView(amount);
            row.addView(space(6), new LinearLayout.LayoutParams(dp(6), 1));
            final int step = group.stepGrams();
            Button minus = button("−", Color.rgb(236, 240, 234), INK, v -> {
                todayLog().addGrams(group, -step);
                saveState();
                renderFoodPreservingScroll();
            });
            Button plus = button("+" + step, GREEN_SOFT, GREEN, v -> {
                todayLog().addGrams(group, step);
                saveState();
                renderFoodPreservingScroll();
            });
            row.addView(minus, new LinearLayout.LayoutParams(dp(42), dp(36)));
            row.addView(space(6), new LinearLayout.LayoutParams(dp(6), 1));
            row.addView(plus, new LinearLayout.LayoutParams(dp(58), dp(36)));
            details.addView(row);
        }
        details.addView(space(8));
        final DayFoodLog waterLog = log;
        LinearLayout waterRow = new LinearLayout(this);
        waterRow.setOrientation(LinearLayout.HORIZONTAL);
        waterRow.setGravity(Gravity.CENTER_VERTICAL);
        boolean waterOk = waterLog.waterMl() >= energyPlan.waterMinMl();
        waterRow.addView(text("饮水", 14, Typeface.BOLD, waterOk ? GREEN : INK),
                new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        TextView waterAmount = text(waterLog.waterMl() + "/" + energyPlan.waterMinMl() + "ml",
                13, waterOk ? Typeface.BOLD : Typeface.NORMAL, waterOk ? GREEN : MUTED);
        waterAmount.setGravity(Gravity.CENTER);
        waterAmount.setMinWidth(dp(82));
        waterAmount.setMinHeight(dp(36));
        waterAmount.setPadding(dp(8), 0, dp(8), 0);
        waterAmount.setBackground(bg(Color.rgb(247, 249, 245), dp(9), LINE, 1));
        waterAmount.setContentDescription("饮水 " + waterLog.waterMl() + " 毫升，点按修改");
        waterAmount.setOnClickListener(v -> editWaterMl());
        waterRow.addView(waterAmount);
        waterRow.addView(space(6), new LinearLayout.LayoutParams(dp(6), 1));
        waterRow.addView(button("−250", Color.rgb(236, 240, 234), INK, v -> {
            todayLog().addWaterMl(-250);
            saveState();
            renderFoodPreservingScroll();
        }), new LinearLayout.LayoutParams(dp(62), dp(36)));
        waterRow.addView(space(6), new LinearLayout.LayoutParams(dp(6), 1));
        waterRow.addView(button("+250", Color.rgb(224, 238, 248), BLUE, v -> {
            todayLog().addWaterMl(250);
            saveState();
            renderFoodPreservingScroll();
        }), new LinearLayout.LayoutParams(dp(62), dp(36)));
        details.addView(waterRow);
        details.addView(space(8));
        TextView help = text("不知道怎么归类？查看记录说明", 12, Typeface.BOLD, BLUE);
        help.setPadding(0, dp(4), 0, dp(4));
        help.setOnClickListener(v -> showFoodLogHelp());
        details.addView(help);
        details.setVisibility(foodLogExpanded ? View.VISIBLE : View.GONE);
        card.addView(details);
        return card;
    }

    private String foodLogOverview(DayFoodLog log) {
        int recordedGroups = 0;
        for (FoodGroup group : FoodGroup.values()) {
            if (log.grams(group) > 0) {
                recordedGroups++;
            }
        }
        StringBuilder summary = new StringBuilder();
        if (recordedGroups == 0) {
            summary.append("还没记录食物");
        } else {
            summary.append("已记 ").append(recordedGroups).append(" 类食物");
        }
        if (!log.entries().isEmpty()) {
            summary.append(" · ").append(log.entries().size()).append(" 笔餐食");
        }
        summary.append(" · 饮水 ").append(log.waterMl()).append("ml");
        return summary.toString();
    }

    private void showFoodLogHelp() {
        new AlertDialog.Builder(this)
                .setTitle("怎么记录更顺手")
                .setMessage("这里记的是今天累计吃了多少。点中间的克数可以直接输入，± 适合随手微调。\n\n"
                        + "加工食品按主料归类：面包馒头记谷类，火腿肠记鱼禽肉蛋，薯片记薯类；"
                        + "纯零食、含糖饮料和酒记到「零食·其他」。\n\n"
                        + "目标值会按你的 " + energyPlan.targetKcal() + " kcal 计划从宝塔推荐区间中换算。")
                .setPositiveButton("知道了", null)
                .show();
    }

    /** 饮水不只有 250ml 一种杯量；点数字可直接记矿泉水瓶、咖啡杯等任意容量。 */
    private void editWaterMl() {
        final int current = todayLog().waterMl();
        final EditText input = numberField("毫升数，如 330");
        input.setText(current > 0 ? String.valueOf(current) : "");
        input.setSelection(input.getText().length());

        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(20), dp(12), dp(20), 0);
        box.addView(text("填今天累计喝了多少毫升；快捷按钮仍可每次加减 250ml。\n"
                        + "今日建议 " + energyPlan.waterMinMl() + "-" + energyPlan.waterMaxMl() + "ml。",
                13, Typeface.NORMAL, MUTED));
        box.addView(space(10));
        box.addView(input);

        new AlertDialog.Builder(this)
                .setTitle("记录 · 饮水")
                .setView(box)
                .setNegativeButton("取消", null)
                .setPositiveButton("设为", (d, w) -> {
                    todayLog().setWaterMl(parseIntField(input, current));
                    saveState();
                    renderFoodPreservingScroll();
                })
                .show();
    }

    /** 局部微调后回到原来的阅读位置，连续点 ± 不会每次都被送回页面顶部。 */
    private void renderFoodPreservingScroll() {
        final int scrollY = mainScrollView == null ? 0 : mainScrollView.getScrollY();
        renderFood();
        if (mainScrollView != null) {
            mainScrollView.post(() -> mainScrollView.scrollTo(0, scrollY));
        }
    }

    /** 今天「确认记入」过的每一笔，各带一个撤销按钮：点错一次不用等到跨日。 */
    private View committedEntriesBlock(DayFoodLog log) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setBackground(bg(Color.rgb(247, 250, 246), dp(10), LINE, 1));
        box.setPadding(dp(12), dp(10), dp(12), dp(10));
        box.addView(text("今天记入的（记错了点「撤销」减回去）", 12, Typeface.BOLD, INK));
        box.addView(space(4));
        List<FoodLogEntry> entries = log.entries();
        for (int i = 0; i < entries.size(); i++) {
            final FoodLogEntry entry = entries.get(i);
            final int index = i;
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(0, dp(4), 0, dp(4));
            LinearLayout labels = new LinearLayout(this);
            labels.setOrientation(LinearLayout.VERTICAL);
            String time = entry.epochMillis() > 0
                    ? new SimpleDateFormat("HH:mm", Locale.CHINA).format(new Date(entry.epochMillis())) + " "
                    : "";
            labels.addView(text(time + entry.label(), 14, Typeface.BOLD, INK));
            labels.addView(text(entry.summary(), 11, Typeface.NORMAL, MUTED));
            row.addView(labels,
                    new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            row.addView(button("撤销", Color.rgb(236, 240, 234), CORAL,
                    v -> confirmUndoFoodEntry(index, entry)),
                    new LinearLayout.LayoutParams(dp(56), dp(34)));
            box.addView(row);
        }
        return box;
    }

    /** 撤销本身也是一次点击，先说清楚要减掉什么，免得撤错了又没法还原。 */
    private void confirmUndoFoodEntry(final int index, final FoodLogEntry entry) {
        new AlertDialog.Builder(this)
                .setTitle("撤销 · " + entry.label())
                .setMessage("今天的记录会减去：" + entry.summary()
                        + "\n\n手动改过的克数不会被减成负数，最多减到 0。")
                .setNegativeButton("不撤", null)
                .setPositiveButton("撤销", (d, w) -> {
                    // 视图可能停在昨天或已被别处改过，对不上就重画，别撤错一笔
                    List<FoodLogEntry> current = todayLog().entries();
                    if (index >= current.size() || current.get(index) != entry) {
                        renderFoodPreservingScroll();
                        return;
                    }
                    FoodLogEntry undone = todayLog().undo(index);
                    if (undone == null) {
                        return;
                    }
                    saveState();
                    Toast.makeText(this, "已撤销：" + undone.label(), Toast.LENGTH_SHORT).show();
                    renderFoodPreservingScroll();
                })
                .show();
    }

    /** 点数字弹出输入框，直接把某类别设为精确克数（不受 ± 步长限制）。 */
    private void editGroupGrams(final FoodGroup group) {
        final int current = todayLog().grams(group);
        final int target = pagodaTargets.gramsFor(group);
        final EditText input = numberField("克数，如 60");
        input.setText(current > 0 ? String.valueOf(current) : "");
        input.setSelection(input.getText().length());

        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(20), dp(12), dp(20), dp(0));
        String sub = target > 0
                ? group.hint() + "\n今日目标 " + target + "g，填今天累计吃了多少克"
                : group.hint() + "\n宝塔外的额外热量，填今天累计吃了多少克";
        box.addView(text(sub, 13, Typeface.NORMAL, MUTED));
        box.addView(space(10));
        box.addView(input);

        new AlertDialog.Builder(this)
                .setTitle("记录 · " + group.label())
                .setView(box)
                .setNegativeButton("取消", null)
                .setPositiveButton("设为", (d, w) -> {
                    todayLog().setGrams(group, parseIntField(input, current));
                    saveState();
                    renderFoodPreservingScroll();
                })
                .show();
    }

    /**
     * 「记一餐」：外卖和零食没法按类别估克数，所以这里的输入单位是「一份菜」而不是「多少克」，
     * 折算成宝塔生重由预设或 AI 完成。
     */
    private void renderQuickLog() {
        currentTab = "food";
        clear();
        content.addView(title("记一餐", "外卖、零食、估不准克数的一餐都在这里"));

        LinearLayout why = card();
        why.addView(section("不用你换算"));
        why.addView(space(4));
        why.addView(text("宝塔的克数是生重：一碗熟米饭看着 200g，只算谷类 80g（生米）。"
                + "下面每一项都已经折算好，你只要说吃了几份。", 13, Typeface.NORMAL, MUTED));
        content.addView(why);
        content.addView(space(10));

        if (!mealDraft.isEmpty()) {
            content.addView(mealDraftCard());
            content.addView(space(10));
        }

        content.addView(mealEstimateCard());
        content.addView(space(10));

        for (MealPreset.Kind kind : MealPreset.Kind.values()) {
            List<MealPreset> inKind = new ArrayList<MealPreset>();
            for (MealPreset preset : mealPresets) {
                if (preset.kind() == kind) {
                    inKind.add(preset);
                }
            }
            if (inKind.isEmpty()) {
                continue;
            }
            LinearLayout group = card();
            group.addView(section(kind.label()));
            group.addView(text(kind.hint(), 12, Typeface.NORMAL, MUTED));
            group.addView(space(8));
            for (MealPreset preset : inKind) {
                group.addView(mealPresetRow(preset));
            }
            content.addView(group);
            content.addView(space(10));
        }

        content.addView(button("返回", Color.rgb(236, 240, 234), INK, v -> {
            harvestMealEstimate();
            renderFood();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
        renderBottomNav();
    }

    private View mealPresetRow(final MealPreset preset) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(0, dp(5), 0, dp(5));
        LinearLayout labels = new LinearLayout(this);
        labels.setOrientation(LinearLayout.VERTICAL);
        int chosen = mealDraft.halvesFor(preset);
        labels.addView(text(preset.name(), 14, Typeface.BOLD, chosen > 0 ? GREEN : INK));
        labels.addView(text(preset.hint(), 11, Typeface.NORMAL, MUTED));
        row.addView(labels, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        if (chosen > 0) {
            TextView count = text(mealDraft.servingLabel(preset), 13, Typeface.BOLD, GREEN);
            count.setGravity(Gravity.CENTER);
            count.setMinWidth(dp(40));
            row.addView(count);
        }
        row.addView(button("＋", GREEN_SOFT, GREEN, v -> {
            harvestMealEstimate();
            mealDraft.addServing(preset);
            renderQuickLog();
        }), new LinearLayout.LayoutParams(dp(46), dp(36)));
        return row;
    }

    private View mealDraftCard() {
        LinearLayout card = card();
        card.addView(section("这一餐要记入"));
        card.addView(space(6));
        for (final MealPreset preset : mealDraft.presets()) {
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(0, dp(3), 0, dp(3));
            row.addView(text(preset.name() + " " + mealDraft.servingLabel(preset), 14, Typeface.BOLD, INK),
                    new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            row.addView(button("−", Color.rgb(236, 240, 234), INK, v -> {
                harvestMealEstimate();
                mealDraft.adjust(preset, -1);
                renderQuickLog();
            }), new LinearLayout.LayoutParams(dp(42), dp(34)));
            row.addView(space(6), new LinearLayout.LayoutParams(dp(6), 1));
            row.addView(button("＋", GREEN_SOFT, GREEN, v -> {
                harvestMealEstimate();
                mealDraft.adjust(preset, 1);
                renderQuickLog();
            }), new LinearLayout.LayoutParams(dp(42), dp(34)));
            card.addView(row);
        }
        if (mealDraft.hasEstimate()) {
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(0, dp(3), 0, dp(3));
            row.addView(text(mealDraft.estimateLabel(), 14, Typeface.BOLD, BLUE),
                    new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            row.addView(button("移除", Color.rgb(236, 240, 234), INK, v -> {
                harvestMealEstimate();
                mealDraft.clearEstimate();
                renderQuickLog();
            }), new LinearLayout.LayoutParams(dp(60), dp(34)));
            card.addView(row);
        }
        card.addView(space(8));
        card.addView(text("合计：" + mealDraft.summary(), 13, Typeface.BOLD, INK));
        card.addView(text("估算约 " + mealDraft.totalKcal() + " kcal（仅供对照）",
                12, Typeface.NORMAL, MUTED));
        card.addView(space(10));
        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        actions.addView(button("清空", Color.rgb(236, 240, 234), INK, v -> {
            harvestMealEstimate();
            mealDraft.clear();
            renderQuickLog();
        }), new LinearLayout.LayoutParams(0, dp(46), 1f));
        actions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        actions.addView(button("确认记入今天", GREEN, Color.WHITE, v -> applyMealDraft()),
                new LinearLayout.LayoutParams(0, dp(46), 2f));
        card.addView(actions);
        return card;
    }

    private View mealEstimateCard() {
        LinearLayout card = card();
        card.addView(section("说不上来？让 AI 估"));
        card.addView(space(4));
        card.addView(text("用一句话描述，或直接拍/选一张餐食照片，AI 拆成宝塔生重克数，"
                + "写入前你还能核对和改。", 12, Typeface.NORMAL, MUTED));
        card.addView(space(8));
        mealEstimateInput = new EditText(this);
        mealEstimateInput.setSingleLine(false);
        mealEstimateInput.setMinLines(1);
        mealEstimateInput.setHint("例如：点了一份黄焖鸡米饭，米饭剩了三分之一，还喝了一杯全糖奶茶");
        mealEstimateInput.setTextColor(INK);
        mealEstimateInput.setHintTextColor(Color.rgb(126, 137, 132));
        mealEstimateInput.setTextSize(15);
        mealEstimateInput.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        mealEstimateInput.setBackground(bg(Color.rgb(249, 251, 247), dp(8), LINE, 1));
        mealEstimateInput.setPadding(dp(12), dp(10), dp(12), dp(10));
        mealEstimateInput.setText(mealEstimateText);
        card.addView(mealEstimateInput, matchWrap());
        card.addView(space(10));
        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        actions.addView(button("按描述估算", BLUE, Color.WHITE, v -> estimateMealFromText()),
                new LinearLayout.LayoutParams(0, dp(46), 1f));
        actions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        actions.addView(button("拍照/选图估算", BLUE, Color.WHITE, v -> pickMealPhoto()),
                new LinearLayout.LayoutParams(0, dp(46), 1f));
        card.addView(actions);
        if (!aiConfigured()) {
            card.addView(space(6));
            card.addView(text("需要先在设置里开启 AI 并填 Key；描述和照片会发送到 Google Gemini。"
                    + "不想联网就用上面的预设，效果够用。", 11, Typeface.NORMAL, MUTED));
        }
        return card;
    }

    private void harvestMealEstimate() {
        if (mealEstimateInput != null) {
            mealEstimateText = mealEstimateInput.getText().toString();
        }
    }

    private void applyMealDraft() {
        if (mealDraft.isEmpty()) {
            return;
        }
        DayFoodLog log = todayLog();
        log.record(new FoodLogEntry("记一餐 · " + mealDraft.itemsLabel(), mealDraft.totalKcal(),
                0, 0, mealDraft.totalGrams(), "", System.currentTimeMillis()));
        String summary = mealDraft.summary();
        mealDraft.clear();
        mealEstimateText = "";
        saveState();
        Toast.makeText(this, "已记入：" + summary, Toast.LENGTH_LONG).show();
        renderFood();
    }

    private void pickMealPhoto() {
        harvestMealEstimate();
        if (!aiConfigured()) {
            promptEnableAi("餐食估算");
            return;
        }
        try {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("image/*");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivityForResult(intent, REQ_PICK_MEAL_PHOTO);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开图片选择器", Toast.LENGTH_SHORT).show();
        }
    }

    private void estimateMealFromText() {
        harvestMealEstimate();
        if (!aiConfigured()) {
            promptEnableAi("餐食估算");
            return;
        }
        final String described = mealEstimateText.trim();
        if (described.length() == 0) {
            Toast.makeText(this, "先写一句你吃了什么", Toast.LENGTH_SHORT).show();
            return;
        }
        final AlertDialog busy = showBusy("AI 正在估算这一餐…");
        geminiClient.generate(aiApiKey, aiModel,
                mealEstimationPrompt() + "\n\n用户描述：" + described,
                new GeminiClient.Callback() {
                    @Override
                    public void onResult(String text) {
                        busy.dismiss();
                        confirmMealEstimate(text, described);
                    }

                    @Override
                    public void onError(String message) {
                        busy.dismiss();
                        Toast.makeText(MainActivity.this, "估算失败（" + message + "），可改用上面的预设",
                                Toast.LENGTH_LONG).show();
                    }
                });
    }

    private void estimateMealFromImage(Uri uri) {
        PreparedImage image = prepareImageForAi(uri);
        if (image == null) {
            Toast.makeText(this, "无法读取这张图片", Toast.LENGTH_SHORT).show();
            return;
        }
        String extra = mealEstimateText.trim();
        String prompt = mealEstimationPrompt() + "\n\n请识别照片里的餐食。"
                + (extra.length() > 0 ? "用户补充：" + extra : "");
        final AlertDialog busy = showBusy("AI 正在看这张照片…");
        geminiClient.generate(aiApiKey, aiModel, prompt, image.bytes, image.mimeType,
                new GeminiClient.Callback() {
                    @Override
                    public void onResult(String text) {
                        busy.dismiss();
                        confirmMealEstimate(text, "照片里的一餐");
                    }

                    @Override
                    public void onError(String message) {
                        busy.dismiss();
                        Toast.makeText(MainActivity.this, "识别失败（" + message + "），可改用上面的预设",
                                Toast.LENGTH_LONG).show();
                    }
                });
    }

    private String mealEstimationPrompt() {
        StringBuilder builder = new StringBuilder();
        builder.append("你是营养师，要把用户吃的一餐拆成《中国居民膳食指南 2022》平衡膳食宝塔的类别克数。\n");
        builder.append("**关键：所有克数一律用生重/干重**，不是熟重也不是成品净重。");
        builder.append("例如一碗熟米饭 200g 要写成 GRAIN 80（生米），100g 面包写成 GRAIN 70（面粉当量），");
        builder.append("100g 北豆腐写成 SOY_NUT 20（大豆当量），奶酪按 10g≈100g 液态奶折成 DAIRY。\n");
        builder.append("类别只能用这些键：GRAIN 谷类、WHOLE_GRAIN 全谷物和杂豆（是 GRAIN 的一部分，不能超过 GRAIN）、");
        builder.append("TUBER 薯类、VEGETABLE 蔬菜、FRUIT 水果、ANIMAL 鱼禽肉蛋、DAIRY 奶及奶制品、");
        builder.append("SOY_NUT 大豆及坚果、OIL 烹调油（含煎炸吸油）、OTHER 宝塔外的零食含糖饮料酒。\n");
        builder.append("只输出 JSON：{\"name\":\"这一餐的简称\",\"kcal\":整数,");
        builder.append("\"groups\":{\"GRAIN\":100,\"ANIMAL\":80},\"note\":\"一句话说明你的估算假设\"}。");
        builder.append("没有的类别就不要写进 groups。分量说不准时按常见的一人份估，宁可略保守。");
        return builder.toString();
    }

    private void confirmMealEstimate(String json, String fallbackName) {
        Map<FoodGroup, Integer> grams = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        String name = fallbackName;
        String note = "";
        int kcal = 0;
        try {
            JSONObject object = new JSONObject(json);
            String parsedName = object.optString("name", "").trim();
            if (parsedName.length() > 0) {
                name = parsedName;
            }
            note = object.optString("note", "").trim();
            kcal = Math.max(0, object.optInt("kcal"));
            JSONObject groupJson = object.optJSONObject("groups");
            if (groupJson != null) {
                Iterator<String> keys = groupJson.keys();
                while (keys.hasNext()) {
                    String key = keys.next();
                    FoodGroup group = FoodGroup.parse(key, null);
                    int value = groupJson.optInt(key);
                    if (group != null && value > 0) {
                        grams.put(group, value);
                    }
                }
            }
        } catch (Exception broken) {
            grams.clear();
        }
        if (grams.isEmpty()) {
            Toast.makeText(this, "没能拆出宝塔类别，可改用上面的预设", Toast.LENGTH_LONG).show();
            return;
        }
        // 全谷物是谷类的子集，AI 偶尔会写反，这里兜住以免打卡出现子集大于父集。
        Integer grain = grams.get(FoodGroup.GRAIN);
        Integer whole = grams.get(FoodGroup.WHOLE_GRAIN);
        if (whole != null && (grain == null || whole > grain)) {
            grams.put(FoodGroup.GRAIN, whole);
        }

        StringBuilder detail = new StringBuilder();
        for (Map.Entry<FoodGroup, Integer> entry : grams.entrySet()) {
            detail.append(entry.getKey().label()).append(" ").append(entry.getValue()).append("g\n");
        }
        detail.append("\n估算约 ").append(kcal).append(" kcal");
        if (note.length() > 0) {
            detail.append("\n\nAI 的假设：").append(note);
        }
        detail.append("\n\n这是估算值，确认后加入待记入列表，还能再改。");

        final Map<FoodGroup, Integer> confirmed = grams;
        final String confirmedName = name;
        final int confirmedKcal = kcal;
        new AlertDialog.Builder(this)
                .setTitle("AI 估算：" + name)
                .setMessage(detail.toString())
                .setNegativeButton("不用", null)
                .setPositiveButton("加入", (d, w) -> {
                    harvestMealEstimate();
                    mealDraft.setEstimate("AI · " + confirmedName, confirmedKcal, confirmed);
                    renderQuickLog();
                })
                .show();
    }

    private View gapSummaryLine() {
        DayFoodLog log = todayLog();
        List<String> gaps = new ArrayList<String>();
        for (FoodGroup group : new FoodGroup[]{FoodGroup.VEGETABLE, FoodGroup.WHOLE_GRAIN,
                FoodGroup.DAIRY, FoodGroup.FRUIT, FoodGroup.SOY_NUT}) {
            int remaining = pagodaTargets.remaining(group, log.grams(group));
            if (remaining > 0) {
                gaps.add(group.label() + remaining + "g");
            }
        }
        if (gaps.isEmpty()) {
            return text("今天宝塔重点类别都达标了，注意油盐别超量。", 13, Typeface.BOLD, GREEN);
        }
        StringBuilder builder = new StringBuilder("今天还差：");
        for (int i = 0; i < gaps.size(); i++) {
            if (i > 0) {
                builder.append("、");
            }
            builder.append(gaps.get(i));
        }
        return text(builder.toString(), 13, Typeface.BOLD, AMBER);
    }

    private View builtinRecipeRow(final BuiltinRecipe recipe, String reason) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setBackground(bg(Color.rgb(247, 250, 246), dp(10), LINE, 1));
        box.setPadding(dp(12), dp(10), dp(12), dp(10));
        box.addView(text(recipe.name(), 16, Typeface.BOLD, INK));
        box.addView(text(recipe.macroLabel(), 12, Typeface.NORMAL, MUTED));
        if (reason != null && reason.length() > 0) {
            box.addView(space(4));
            box.addView(text(reason, 13, Typeface.NORMAL, GREEN));
        }
        box.addView(space(8));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(button("看做法", BLUE, Color.WHITE, v -> renderBuiltinRecipeDetail(recipe)),
                new LinearLayout.LayoutParams(0, dp(40), 1f));
        row.addView(space(8), new LinearLayout.LayoutParams(dp(8), 1));
        row.addView(button("记入今日", GREEN, Color.WHITE, v -> markRecipeEaten(recipe)),
                new LinearLayout.LayoutParams(0, dp(40), 1f));
        box.addView(row);
        return box;
    }

    private void markRecipeEaten(BuiltinRecipe recipe) {
        todayLog().record(new FoodLogEntry(recipe.name(), recipe.kcal(), recipe.proteinG(),
                recipe.fiberG(), recipe.allGroupGrams(), recipe.id(), System.currentTimeMillis()));
        saveState();
        Toast.makeText(this, "已记入：" + recipe.name() + "（记错了可在今日打卡里撤销）",
                Toast.LENGTH_SHORT).show();
        if ("food".equals(currentTab)) {
            renderFood();
        }
    }

    /** 我的菜谱也能一键记入今日，走的是同一条可撤销的记录路径。 */
    private void markRecipeEaten(Recipe recipe) {
        if (!recipe.hasNutrition()) {
            Toast.makeText(this, "这道菜还没有营养估算，先估算一次再记入", Toast.LENGTH_SHORT).show();
            return;
        }
        todayLog().record(new FoodLogEntry(recipe.name, recipe.kcal, recipe.proteinG,
                recipe.fiberG, recipe.groupGrams, recipe.builtinId, System.currentTimeMillis()));
        saveState();
        Toast.makeText(this, "已记入：" + recipe.name + "（记错了可在今日打卡里撤销）",
                Toast.LENGTH_SHORT).show();
        renderFood();
    }

    /**
     * 给自己录的菜谱补上营养估算：有了它这道菜才进得了按缺口推荐的候选池，
     * 也才能一键记入今日。估不准无所谓，宝塔本来就是量级判断。
     */
    private void estimateRecipeNutrition(final Recipe recipe) {
        if (!aiConfigured()) {
            promptEnableAi("营养估算");
            return;
        }
        Toast.makeText(this, "正在估算营养…", Toast.LENGTH_SHORT).show();
        StringBuilder prompt = new StringBuilder();
        prompt.append("你是营养师。请估算这道菜「单人份」的营养，依据《中国食物成分表》常见值。\n");
        prompt.append("菜名：").append(recipe.name).append("\n");
        if (!recipe.ingredients.isEmpty()) {
            prompt.append("配料：").append(join(recipe.ingredients)).append("\n");
        }
        for (RecipeStep step : recipe.steps) {
            prompt.append("步骤：").append(step.text).append("\n");
        }
        prompt.append("只返回 JSON，不要 Markdown：")
                .append("{\"kcal\":整数,\"protein_g\":整数,\"fiber_g\":整数,")
                .append("\"pagoda_grams\":{类别:生重克数}}。")
                .append("pagoda_grams 的类别只能用这些键：").append(pagodaKeyList()).append("；")
                .append("一律填生重/干重（一碗熟米饭记 GRAIN 80，不是熟重 200），没有的类别就不要写。")
                .append("配料写了用量就按用量算，没写就按一份家常菜的常见量估。");
        geminiClient.generate(aiApiKey, aiModel, prompt.toString(), new GeminiClient.Callback() {
            @Override
            public void onResult(String text) {
                if (!applyNutritionEstimate(recipe, text)) {
                    Toast.makeText(MainActivity.this, "估算结果不可用，再试一次", Toast.LENGTH_SHORT).show();
                    return;
                }
                saveState();
                Toast.makeText(MainActivity.this, "已估算：" + recipe.kcal + " kcal", Toast.LENGTH_SHORT).show();
                renderRecipeDetail(recipe);
            }

            @Override
            public void onError(String message) {
                Toast.makeText(MainActivity.this, "估算失败：" + message, Toast.LENGTH_LONG).show();
            }
        });
    }

    private boolean applyNutritionEstimate(Recipe recipe, String text) {
        try {
            JSONObject object = new JSONObject(text);
            int kcal = Math.max(0, object.optInt("kcal", 0));
            JSONObject pagoda = object.optJSONObject("pagoda_grams");
            if (kcal == 0 && pagoda == null) {
                return false;
            }
            recipe.kcal = kcal;
            recipe.proteinG = Math.max(0, object.optInt("protein_g", 0));
            recipe.fiberG = Math.max(0, object.optInt("fiber_g", 0));
            recipe.groupGrams.clear();
            if (pagoda != null) {
                for (FoodGroup group : FoodGroup.values()) {
                    int grams = pagoda.optInt(group.name(), 0);
                    if (grams > 0) {
                        recipe.groupGrams.put(group, grams);
                    }
                }
            }
            return recipe.hasNutrition();
        } catch (Exception ignored) {
            return false;
        }
    }

    private void renderBuiltinRecipeDetail(final BuiltinRecipe recipe) {
        currentTab = "food";
        clear();
        content.addView(title(recipe.name(), join(recipe.mealSlots()) + " · " + join(recipe.tags())));

        LinearLayout macro = card();
        macro.addView(section("营养（单人份，估算）"));
        macro.addView(space(4));
        macro.addView(text(recipe.macroLabel(), 15, Typeface.BOLD, BLUE));
        macro.addView(space(6));
        StringBuilder groups = new StringBuilder();
        for (Map.Entry<FoodGroup, Integer> entry : recipe.allGroupGrams().entrySet()) {
            if (groups.length() > 0) {
                groups.append(" · ");
            }
            groups.append(entry.getKey().label()).append(" ").append(entry.getValue()).append("g");
        }
        macro.addView(text("宝塔构成：" + groups, 13, Typeface.NORMAL, MUTED));
        content.addView(macro);

        LinearLayout ingredients = card();
        ingredients.addView(section("食材"));
        ingredients.addView(space(4));
        for (String item : recipe.ingredients()) {
            ingredients.addView(text("· " + item, 14, Typeface.NORMAL, INK));
        }
        content.addView(ingredients);

        LinearLayout steps = card();
        steps.addView(section("做法"));
        steps.addView(space(4));
        int index = 1;
        for (String step : recipe.steps()) {
            steps.addView(text(index + ". " + step, 14, Typeface.NORMAL, INK));
            steps.addView(space(4));
            index++;
        }
        content.addView(steps);

        LinearLayout why = card();
        why.addView(section("为什么这么搭配"));
        why.addView(space(4));
        why.addView(text(recipe.rationale(), 14, Typeface.NORMAL, INK));
        why.addView(space(8));
        for (String ref : recipe.refs()) {
            why.addView(text("· " + ref, 12, Typeface.NORMAL, MUTED));
            why.addView(space(4));
        }
        content.addView(why);

        LinearLayout actions = card();
        actions.addView(button("我吃了这份 · 记入今日", GREEN, Color.WHITE, v -> {
            markRecipeEaten(recipe);
            renderFood();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));
        actions.addView(space(8));
        Recipe saved = savedCopyOfBuiltin(recipe.id());
        if (saved == null) {
            actions.addView(button("收进我的菜谱", BLUE, Color.WHITE,
                    v -> saveBuiltinToLibrary(recipe)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
            actions.addView(space(4));
            actions.addView(text("收进去之后可以评分、写点评、加成品照，和自己录的菜谱一样。",
                    11, Typeface.NORMAL, MUTED));
            actions.addView(space(8));
        } else {
            actions.addView(button("已在我的菜谱 · 去看看", Color.rgb(236, 240, 234), INK,
                    v -> renderRecipeDetail(saved)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
            actions.addView(space(8));
        }
        actions.addView(button("返回", Color.rgb(236, 240, 234), INK, v -> renderFood()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        content.addView(actions);
        renderBottomNav();
    }

    // ------------------------------------------------------------------ //
    // 周期训练计划：评估 → 目标设定 → 分阶段计划 → 按日开练
    // ------------------------------------------------------------------ //

    private View programCard() {
        LinearLayout card = card();
        if (program == null) {
            card.addView(section("周期训练计划"));
            card.addView(space(6));
            card.addView(text("按目标生成 8 周分阶段计划（依据 ACSM/NSCA 指南）：先做 1 分钟状态评估，"
                    + "计划强度会匹配你的水平；每次训练不同部位，每个肌群每周至少练 2 次。", 14, Typeface.NORMAL, MUTED));
            card.addView(space(10));
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.addView(button(assessment == null ? "开始状态评估" : "重新评估", GREEN, Color.WHITE,
                            v -> renderAssessmentForm()),
                    new LinearLayout.LayoutParams(0, dp(46), 1f));
            if (assessment != null) {
                row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
                row.addView(button("设定目标生成计划", BLUE, Color.WHITE, v -> renderProgramSetup()),
                        new LinearLayout.LayoutParams(0, dp(46), 1f));
            }
            card.addView(row);
            if (assessment != null) {
                card.addView(space(8));
                card.addView(text("当前评估（" + assessmentDate + "）：" + assessment.level().label()
                        + " · 强度上限 " + assessment.intensityCap().label(), 13, Typeface.BOLD, BLUE));
            }
            return card;
        }

        if (schedule == null || schedule.isEmpty()) {
            card.addView(section(program.title()));
            card.addView(space(6));
            card.addView(text("这个计划还没有排进日历，重新生成一次就能拿到每天的动作安排。",
                    14, Typeface.NORMAL, MUTED));
            card.addView(space(10));
            card.addView(button("重新生成计划", GREEN, Color.WHITE, v -> renderProgramSetup()),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(46)));
            return card;
        }

        refreshScheduleStatus();
        int done = schedule.doneCount();
        int total = schedule.totalCount();
        final ScheduledSession next = schedule.todayOrNext(todayEpochDay());
        card.addView(section(program.title()));
        card.addView(space(4));
        if (next == null) {
            card.addView(text("🎉 全部 " + total + " 次训练已完成！建议重新评估状态，再开启下一个周期。",
                    15, Typeface.BOLD, GREEN));
            card.addView(space(10));
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.addView(button("重新评估", GREEN, Color.WHITE, v -> renderAssessmentForm()),
                    new LinearLayout.LayoutParams(0, dp(44), 1f));
            row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
            row.addView(button("查看日历", Color.rgb(236, 240, 234), INK, v -> renderCalendar()),
                    new LinearLayout.LayoutParams(0, dp(44), 1f));
            card.addView(row);
            return card;
        }

        ProgramPhase phase = program.phaseForWeek(next.week());
        boolean isToday = next.epochDay() == todayEpochDay();
        card.addView(text("第 " + next.week() + "/" + program.totalWeeks() + " 周 · " + phase.name()
                + " · 已完成 " + done + "/" + total + " 次", 13, Typeface.BOLD, BLUE));
        card.addView(space(6));
        card.addView(progressBar(done / (float) total));
        card.addView(space(10));

        // 本周日历：一眼看到哪天练什么、哪天漏了。
        LinearLayout weekRow = new LinearLayout(this);
        weekRow.setOrientation(LinearLayout.HORIZONTAL);
        long weekStart = ProgramSchedule.startOfWeek(todayEpochDay());
        boolean thisWeekHasSessions = false;
        for (int i = 0; i < 7 && !thisWeekHasSessions; i++) {
            thisWeekHasSessions = !schedule.onDate(weekStart + i).isEmpty();
        }
        if (!thisWeekHasSessions) {
            // 本周没有安排（比如计划从下周一开始），就显示下一次训练所在的那一周。
            weekStart = ProgramSchedule.startOfWeek(next.epochDay());
        }
        for (int i = 0; i < 7; i++) {
            long day = weekStart + i;
            List<ScheduledSession> onDay = schedule.onDate(day);
            String label = WEEKDAY_SHORT[i];
            int color = MUTED;
            int background = Color.rgb(247, 249, 245);
            if (!onDay.isEmpty()) {
                ScheduledSession session = onDay.get(0);
                label += " " + session.focus().label();
                if (session.status() == ScheduledSession.Status.DONE) {
                    label = "✓ " + label;
                    color = GREEN;
                    background = GREEN_SOFT;
                } else if (session.status() == ScheduledSession.Status.MISSED) {
                    label = "✗ " + label;
                    color = CORAL;
                } else {
                    color = INK;
                    background = Color.rgb(236, 240, 234);
                }
            }
            TextView chip = text(label, 12, day == todayEpochDay() ? Typeface.BOLD : Typeface.NORMAL, color);
            chip.setPadding(dp(9), dp(6), dp(9), dp(6));
            chip.setBackground(bg(background, dp(8),
                    day == todayEpochDay() ? GREEN : LINE, 1));
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            lp.setMargins(0, 0, dp(6), 0);
            weekRow.addView(chip, lp);
        }
        card.addView(wrapScroll(weekRow));
        card.addView(space(8));

        List<WorkoutItem> nextItems = scheduledItems(next, phase);
        card.addView(text((isToday ? "今天：" : dateLabel(next.epochDay()) + "：")
                + next.focus().label() + " · " + nextItems.size() + " 个动作 · 预计 "
                + timeModel().sessionMinutes(nextItems) + " 分钟", 14, Typeface.BOLD, INK));
        card.addView(text("本阶段：" + phase.prescription().compactLabel(), 13, Typeface.NORMAL, MUTED));
        if (phase.aerobicMinutesPerWeek() > 0) {
            card.addView(text("有氧：" + phase.aerobicNote(), 13, Typeface.NORMAL, MUTED));
        }
        card.addView(space(10));

        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        actions.addView(button((isToday ? "开今日训练：" : "查看下一次：") + next.focus().label(),
                        GREEN, Color.WHITE, v -> renderScheduledDay(next.key())),
                new LinearLayout.LayoutParams(0, dp(48), 2f));
        actions.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        actions.addView(button("日历", Color.rgb(236, 240, 234), INK, v -> renderCalendar()),
                new LinearLayout.LayoutParams(0, dp(48), 1f));
        card.addView(actions);
        return card;
    }

    private View progressBar(float fraction) {
        FrameLayout track = new FrameLayout(this);
        track.setBackground(bg(Color.rgb(236, 240, 234), dp(5), LINE, 0));
        View fill = new View(this);
        fill.setBackground(bg(GREEN, dp(5), GREEN, 0));
        int width = Math.max(dp(8), (int) (fraction * (getResources().getDisplayMetrics().widthPixels - dp(76))));
        track.addView(fill, new FrameLayout.LayoutParams(width, dp(10)));
        LinearLayout wrap = new LinearLayout(this);
        wrap.addView(track, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(10)));
        return wrap;
    }


    private void renderAssessmentForm() {
        renderAssessmentForm(false, false);
    }

    private void renderAssessmentForm(boolean prefillExisting, boolean returnToSettings) {
        currentTab = returnToSettings ? "settings" : "training";
        clear();
        content.addView(title("体能评估", "1 分钟：安全筛查 + 训练史 + 可选自测"));

        if (assessment != null) {
            LinearLayout current = card();
            current.addView(smallLabel("当前评估（" + (assessmentDate.length() == 0 ? "日期未记录" : assessmentDate) + "）"));
            current.addView(text(assessment.level().label() + " · 强度上限 " + assessment.intensityCap().label(),
                    16, Typeface.BOLD, assessment.medicalClearanceAdvised() ? CORAL : INK));
            if (prefillExisting && assessmentInput == null) {
                current.addView(space(6));
                current.addView(noteBox("这是旧版评估，当时未保存原始问卷答案，因此无法准确回填。"
                        + "请按现在的情况重新填写；在点击保存前，原评估不会改变。", AMBER));
            }
            content.addView(current);
        }

        LinearLayout safety = card();
        safety.addView(section("① 安全筛查（PAR-Q+ 简化）"));
        safety.addView(space(4));
        safety.addView(text("过去回答均为「否」才适合直接开始；任一「是」都建议先咨询医生，计划会自动降为低强度。",
                13, Typeface.NORMAL, MUTED));
        safety.addView(space(6));
        String[] questions = {
                "医生是否说过你有心脏问题、只能做医生推荐的运动？",
                "体力活动时是否感到胸痛？",
                "近一个月内，安静状态下是否出现过胸痛？",
                "是否曾因头晕失去平衡或失去知觉？",
                "是否有会因运动加重的骨骼/关节问题？",
                "是否正在服用治疗血压或心脏病的药物？",
                "是否有其他不适合体力活动的原因？"};
        final List<CheckBox> safetyBoxes = new ArrayList<CheckBox>();
        boolean[] savedSafety = assessmentInput == null ? new boolean[7] : new boolean[]{
                assessmentInput.heartCondition(), assessmentInput.chestPainActivity(),
                assessmentInput.chestPainRest(), assessmentInput.dizziness(),
                assessmentInput.boneJointProblem(), assessmentInput.bloodPressureMeds(),
                assessmentInput.otherReason()};
        for (int i = 0; i < questions.length; i++) {
            CheckBox box = new CheckBox(this);
            box.setText(questions[i]);
            box.setTextColor(INK);
            box.setTextSize(14);
            box.setChecked(prefillExisting && savedSafety[i]);
            safetyBoxes.add(box);
            safety.addView(box);
        }
        content.addView(safety);

        LinearLayout history = card();
        history.addView(section("② 训练史"));
        history.addView(space(6));
        history.addView(smallLabel("规律力量训练累计多少个月？（中断超过 3 个月就从中断后算起）"));
        final EditText monthsField = numberField("如：8");
        history.addView(monthsField, matchWrap());
        history.addView(space(8));
        history.addView(smallLabel("近 3 个月平均每周训练几次？"));
        final EditText weeklyField = numberField("如：3");
        if (prefillExisting && assessmentInput != null) {
            monthsField.setText(String.valueOf(assessmentInput.trainingMonths()));
            weeklyField.setText(String.valueOf(assessmentInput.weeklySessions()));
        }
        history.addView(weeklyField, matchWrap());
        content.addView(history);

        LinearLayout tests = card();
        tests.addView(section("③ 体能自测（可选，不测则按训练史定级）"));
        tests.addView(space(4));
        tests.addView(text("自测偏弱时会更稳妥地降一级起步；4 周后可重测上调。", 13, Typeface.NORMAL, MUTED));
        tests.addView(space(6));
        tests.addView(smallLabel("标准俯卧撑一次最多做几个？"));
        final EditText pushupField = numberField("留空 = 未测");
        tests.addView(pushupField, matchWrap());
        tests.addView(space(8));
        tests.addView(smallLabel("平板支撑最长坚持多少秒？"));
        final EditText plankField = numberField("留空 = 未测");
        tests.addView(plankField, matchWrap());
        tests.addView(space(8));
        tests.addView(smallLabel("60 秒内标准徒手深蹲能做几个？"));
        final EditText squatField = numberField("留空 = 未测");
        if (prefillExisting && assessmentInput != null) {
            if (assessmentInput.pushupMax() >= 0) pushupField.setText(String.valueOf(assessmentInput.pushupMax()));
            if (assessmentInput.plankSeconds() >= 0) plankField.setText(String.valueOf(assessmentInput.plankSeconds()));
            if (assessmentInput.squatCount60s() >= 0) squatField.setText(String.valueOf(assessmentInput.squatCount60s()));
        }
        tests.addView(squatField, matchWrap());
        content.addView(tests);

        LinearLayout actions = card();
        actions.addView(button(prefillExisting && assessment != null ? "保存评估修改" : "生成评估结论", GREEN, Color.WHITE, v -> {
            AssessmentInput.Builder builder = new AssessmentInput.Builder()
                    .safetyFlags(safetyBoxes.get(0).isChecked(), safetyBoxes.get(1).isChecked(),
                            safetyBoxes.get(2).isChecked(), safetyBoxes.get(3).isChecked(),
                            safetyBoxes.get(4).isChecked(), safetyBoxes.get(5).isChecked(),
                            safetyBoxes.get(6).isChecked())
                    .history(parseIntField(monthsField, 0), parseIntField(weeklyField, 0));
            int pushup = parseIntField(pushupField, -1);
            int plank = parseIntField(plankField, -1);
            int squat = parseIntField(squatField, -1);
            if (pushup >= 0) {
                builder.pushupMax(pushup);
            }
            if (plank >= 0) {
                builder.plankSeconds(plank);
            }
            if (squat >= 0) {
                builder.squatCount60s(squat);
            }
            assessmentInput = builder.build();
            assessment = new FitnessAssessment().evaluate(assessmentInput);
            assessmentDate = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA).format(new Date());
            if (safetyBoxes.get(4).isChecked()) {
                Toast.makeText(this, "提醒：请在设置里同步标记伤痛部位，推荐会避开高压力动作",
                        Toast.LENGTH_LONG).show();
            }
            rebuildProgramAfterAssessmentChange();
            invalidatePreparedWorkoutAfterAssessmentChange();
            saveState();
            if (returnToSettings) renderSettings(); else renderProgramSetup();
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(50)));
        actions.addView(space(8));
        actions.addView(button("返回", Color.rgb(236, 240, 234), INK,
                        v -> { if (returnToSettings) renderSettings(); else renderTraining(); }),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        actions.addView(space(8));
        actions.addView(text(GuidelineRefs.PARQ + "。" + GuidelineRefs.LEVEL_NOTE + "。",
                12, Typeface.NORMAL, MUTED));
        content.addView(actions);
        renderBottomNav();
    }

    private EditText numberField(String hint) {
        EditText field = new EditText(this);
        field.setHint(hint);
        field.setSingleLine(true);
        field.setInputType(InputType.TYPE_CLASS_NUMBER);
        field.setTextColor(INK);
        field.setHintTextColor(Color.rgb(150, 160, 155));
        field.setTextSize(15);
        field.setBackground(bg(Color.rgb(249, 251, 247), dp(8), LINE, 1));
        field.setPadding(dp(12), dp(9), dp(12), dp(9));
        return field;
    }

    private int parseIntField(EditText field, int fallback) {
        try {
            String value = field.getText().toString().trim();
            return value.length() == 0 ? fallback : Integer.parseInt(value);
        } catch (Exception broken) {
            return fallback;
        }
    }

    private void renderProgramSetup() {
        currentTab = "training";
        clear();
        content.addView(title("设定周期目标", "按目标和可练天数生成 8 周计划"));
        content.addView(reviewScopeButton(this::renderProgramSetup), fullButton());

        if (assessment != null) {
            LinearLayout summary = card();
            summary.addView(smallLabel("评估结论（" + assessmentDate + "）"));
            summary.addView(text(assessment.level().label() + " · 强度上限 " + assessment.intensityCap().label(),
                    17, Typeface.BOLD, INK));
            summary.addView(text(assessment.level().summary(), 13, Typeface.NORMAL, MUTED));
            for (String note : assessment.notes()) {
                summary.addView(space(4));
                summary.addView(text("· " + note, 13, Typeface.NORMAL,
                        assessment.medicalClearanceAdvised() ? CORAL : MUTED));
            }
            content.addView(summary);
        }

        LinearLayout goalCard = card();
        goalCard.addView(section("训练目标"));
        goalCard.addView(space(6));
        final RadioGroup goalGroup = new RadioGroup(this);
        PlanGoal[] goals = PlanGoal.values();
        for (int i = 0; i < goals.length; i++) {
            RadioButton radio = new RadioButton(this);
            radio.setId(9100 + i);
            radio.setText(goals[i].label() + " —— " + goals[i].summary());
            radio.setTextColor(INK);
            radio.setTextSize(14);
            if (i == 0) {
                radio.setChecked(true);
            }
            goalGroup.addView(radio);
        }
        goalCard.addView(goalGroup);
        content.addView(goalCard);

        LinearLayout daysCard = card();
        daysCard.addView(section("每周能练几天"));
        daysCard.addView(space(6));
        final RadioGroup daysGroup = new RadioGroup(this);
        daysGroup.setOrientation(RadioGroup.HORIZONTAL);
        int[] options = {2, 3, 4, 5};
        for (int i = 0; i < options.length; i++) {
            RadioButton radio = new RadioButton(this);
            radio.setId(9200 + i);
            radio.setText(options[i] + " 天");
            radio.setTextColor(INK);
            if (options[i] == 3) {
                radio.setChecked(true);
            }
            daysGroup.addView(radio);
        }
        daysCard.addView(daysGroup);
        daysCard.addView(space(6));
        daysCard.addView(text("分化随天数自动选择：2 天全身×2；3 天全身 A/B/C；4 天上/下；5 天推/拉/腿+上/下。"
                + "任何一种都保证每个肌群每周至少 2 次。", 13, Typeface.NORMAL, MUTED));
        content.addView(daysCard);

        // 训练放在每周的哪几天——日历要落到具体日期，漏练才有意义。
        final Set<Integer> pickedWeekdays = new LinkedHashSet<Integer>(
                programWeekdays.isEmpty() ? ProgramSchedule.defaultWeekdays(3) : programWeekdays);
        LinearLayout weekdayCard = card();
        weekdayCard.addView(section("每周哪几天练"));
        weekdayCard.addView(space(6));
        final LinearLayout weekdayRow = new LinearLayout(this);
        weekdayRow.setOrientation(LinearLayout.HORIZONTAL);
        final Button[] weekdayChips = new Button[7];
        for (int i = 0; i < 7; i++) {
            final int weekday = i + 1;
            weekdayChips[i] = chip(WEEKDAY_LABELS[i], pickedWeekdays.contains(weekday), null);
            final Button chip = weekdayChips[i];
            chip.setOnClickListener(v -> {
                if (pickedWeekdays.contains(weekday)) {
                    pickedWeekdays.remove(weekday);
                } else {
                    pickedWeekdays.add(weekday);
                }
                styleChip(chip, pickedWeekdays.contains(weekday));
            });
            weekdayRow.addView(chip);
        }
        weekdayCard.addView(wrapScroll(weekdayRow));
        weekdayCard.addView(space(6));
        weekdayCard.addView(text("选不够天数会自动补齐；尽量隔天练，给肌肉留恢复时间。"
                + "漏练不会顺延——周期化的强度是按周设计的，顺延会把曲线拉平。",
                13, Typeface.NORMAL, MUTED));
        content.addView(weekdayCard);

        LinearLayout aiCard = card();
        aiCard.addView(section("让 AI 参与挑动作"));
        aiCard.addView(space(6));
        final CheckBox aiToggle = new CheckBox(this);
        aiToggle.setText("生成计划时用 AI 在安全候选里挑动作");
        aiToggle.setTextColor(INK);
        aiToggle.setChecked(programUseAi && aiConfigured());
        aiToggle.setEnabled(aiConfigured());
        aiCard.addView(aiToggle);
        aiCard.addView(space(4));
        aiCard.addView(text(aiConfigured()
                        ? "伤痛、器械、证据过滤仍然在本机完成，AI 只能在过滤后的候选里选和排序，"
                        + "组数/次数/休息由周期计划决定，AI 不参与。你的伤痛数据不会发送。"
                        : "需要先在「设置 → AI 推荐」开启并填 API Key。关闭时用本地槽位编排，效果一样可用。",
                13, Typeface.NORMAL, MUTED));
        content.addView(aiCard);

        LinearLayout actions = card();
        actions.addView(button("生成 8 周周期计划", GREEN, Color.WHITE, v -> {
            int goalIndex = Math.max(0, goalGroup.getCheckedRadioButtonId() - 9100);
            int daysIndex = Math.max(0, daysGroup.getCheckedRadioButtonId() - 9200);
            PlanGoal goal = PlanGoal.values()[Math.min(goalIndex, PlanGoal.values().length - 1)];
            int days = new int[]{2, 3, 4, 5}[Math.min(daysIndex, 3)];
            TrainingLevel level = assessment == null ? TrainingLevel.BEGINNER : assessment.level();
            programUseAi = aiToggle.isChecked();
            generateProgram(goal, level, days, new ArrayList<Integer>(pickedWeekdays));
        }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(50)));
        actions.addView(space(8));
        actions.addView(button("返回", Color.rgb(236, 240, 234), INK, v -> renderTraining()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        if (assessment == null) {
            actions.addView(space(8));
            actions.addView(text("还没做状态评估：将按初级水平生成。建议先评估，强度更贴合。",
                    13, Typeface.NORMAL, CORAL));
        }
        content.addView(actions);
        renderBottomNav();
    }

    // --------------------------------------------------- 生成计划（可选 AI 参与）

    /**
     * 生成 8 周计划并一次性把每天的动作排好。
     * AI 只影响「每个槽位优先选哪个动作」；安全过滤、跨天去重、组数/次数/休息都不归它管。
     */
    private void generateProgram(PlanGoal goal, TrainingLevel level, int days,
            List<Integer> weekdays) {
        final TrainingProgram target = new ProgramBuilder().build(goal, level, days, assessmentCap());
        List<Integer> picked = new ArrayList<Integer>(weekdays);
        Collections.sort(picked);
        // 选的天数不够就用默认排布补齐，保证每周的次数对得上。
        for (Integer weekday : ProgramSchedule.defaultWeekdays(target.daysPerWeek())) {
            if (picked.size() >= target.daysPerWeek()) {
                break;
            }
            if (!picked.contains(weekday)) {
                picked.add(weekday);
            }
        }
        Collections.sort(picked);
        final List<Integer> finalWeekdays = picked.subList(0,
                Math.min(picked.size(), Math.max(target.daysPerWeek(), 1)));

        if (!programUseAi || !aiConfigured()) {
            applyGeneratedProgram(target, finalWeekdays, null, false);
            return;
        }
        aiThinking = true;
        renderTraining();
        Toast.makeText(this, "正在让 AI 挑动作…", Toast.LENGTH_SHORT).show();
        String prompt = buildProgramPrompt(target);
        geminiClient.generate(aiApiKey, aiModel, prompt, new GeminiClient.Callback() {
            @Override
            public void onResult(String text) {
                Map<String, Map<String, List<String>>> preferences = parseProgramAi(text, target);
                aiThinking = false;
                applyGeneratedProgram(target, finalWeekdays, preferences, preferences != null);
            }

            @Override
            public void onError(String message) {
                aiThinking = false;
                Toast.makeText(MainActivity.this, "AI 暂时不可用（" + message + "），已用本地编排",
                        Toast.LENGTH_LONG).show();
                applyGeneratedProgram(target, finalWeekdays, null, false);
            }
        });
    }

    private void applyGeneratedProgram(TrainingProgram target, List<Integer> weekdays,
            final Map<String, Map<String, List<String>>> preferences, boolean fromAi) {
        program = target;
        programWeekdays.clear();
        programWeekdays.addAll(weekdays);
        schedule = ProgramSchedule.build(target, todayEpochDay(), weekdays,
                new ProgramSchedule.DayComposer() {
                    @Override
                    public ProgramComposer.ComposedDay compose(int week, int dayIndex,
                            ProgramFocus focus, ProgramPhase phase, List<String> recentIds) {
                        RecommendationInput input = programInput(phase, focus);
                        Map<String, List<String>> slotPreferences = preferences == null
                                ? null : preferences.get(focus.name());
                        return ProgramComposer.composeDay(focus, phase.prescription(),
                                engine().safeCandidates(input), exerciseCountFor(phase, focus),
                                recentIds, favoriteIds, slotPreferences);
                    }
                });
        pendingProgramKey = "";
        calendarAnchorEpochDay = todayEpochDay();
        saveState();
        Toast.makeText(this, (fromAi ? "AI 参与生成：" : "已生成：") + program.title()
                + "（" + schedule.totalCount() + " 次训练已排进日历）", Toast.LENGTH_LONG).show();
        renderCalendar();
    }

    /**
     * 只问 AI 一件事：每个分化的每个动作模式槽位，按顺序推荐哪几个动作。
     * 候选已经在本机按伤痛/器械/证据过滤过——伤痛数据本身不会发出去，只发过滤后的动作清单。
     */
    private String buildProgramPrompt(TrainingProgram target) {
        StringBuilder builder = new StringBuilder();
        builder.append("你是健身教练助手。下面的候选动作已经按用户的身体状况、可用器械和证据等级在本地过滤过，")
                .append("你只能从这些候选里挑，绝对不要臆造列表之外的动作。\n");
        builder.append("用户：").append(target.level().label()).append("，目标 ")
                .append(target.goal().label()).append("，每周练 ").append(target.daysPerWeek())
                .append(" 天，分化是 ").append(target.splitName()).append("。\n");
        builder.append("组数、次数、休息由周期计划决定，你不用管，只负责挑动作。\n\n");

        Set<String> emitted = new LinkedHashSet<String>();
        StringBuilder pool = new StringBuilder();
        StringBuilder asks = new StringBuilder();
        Set<ProgramFocus> focuses = new LinkedHashSet<ProgramFocus>(target.weekSplit());
        for (ProgramFocus focus : focuses) {
            ProgramPhase phase = target.phaseForWeek(1);
            List<Exercise> safe = engine().safeCandidates(programInput(phase, focus));
            asks.append("分化 ").append(focus.name()).append("（").append(focus.label())
                    .append("）需要填的槽位：");
            List<ProgramComposer.Slot> slots =
                    ProgramComposer.slotsFor(focus, exerciseCountFor(phase, focus));
            for (ProgramComposer.Slot slot : slots) {
                asks.append(slot.key()).append("（").append(slot.label()).append("） ");
                for (Exercise exercise : ProgramComposer.candidatesFor(slot, focus, safe,
                        new LinkedHashSet<String>(), new ArrayList<String>(), favoriteIds,
                        AI_CANDIDATES_PER_SLOT)) {
                    if (emitted.add(exercise.id())) {
                        pool.append(exercise.id()).append(" | ").append(exercise.name())
                                .append(" | ").append(join(exercise.targetRegions()))
                                .append(" | ").append(join(exercise.movementPatterns()))
                                .append(" | ").append(exercise.difficulty()).append("\n");
                    }
                }
            }
            asks.append("\n");
        }
        builder.append("候选动作（id | 名称 | 部位 | 动作模式 | 难度）：\n").append(pool).append("\n");
        builder.append(asks).append("\n");
        builder.append("请为每个分化的每个槽位，从候选里按推荐顺序给 3-4 个动作 id")
                .append("（第一个是最推荐的；给多个是为了让不同训练日能错开、不总是同一个动作）。\n");
        builder.append("只返回 JSON：{\"focus\": {\"分化名\": {\"槽位key\": [\"动作id\", ...]}}}，")
                .append("不要输出别的内容。分化名用上面给的大写英文名，槽位 key 原样照抄。");
        return builder.toString();
    }

    /** 校验 AI 返回：不在候选池里的 id 一律丢掉，槽位对不上的也丢掉。 */
    private Map<String, Map<String, List<String>>> parseProgramAi(String text, TrainingProgram target) {
        try {
            JSONObject root = new JSONObject(text);
            JSONObject focusMap = root.optJSONObject("focus");
            if (focusMap == null) {
                return null;
            }
            Set<String> known = new LinkedHashSet<String>();
            for (Exercise exercise : allExercises()) {
                known.add(exercise.id());
            }
            Map<String, Map<String, List<String>>> result =
                    new HashMap<String, Map<String, List<String>>>();
            Iterator<String> focusKeys = focusMap.keys();
            while (focusKeys.hasNext()) {
                String focusName = focusKeys.next();
                if (ProgramFocus.parse(focusName, null) == null) {
                    continue;
                }
                JSONObject slots = focusMap.optJSONObject(focusName);
                if (slots == null) {
                    continue;
                }
                Map<String, List<String>> perSlot = new HashMap<String, List<String>>();
                Iterator<String> slotKeys = slots.keys();
                while (slotKeys.hasNext()) {
                    String slotKey = slotKeys.next();
                    JSONArray ids = slots.optJSONArray(slotKey);
                    if (ids == null) {
                        continue;
                    }
                    List<String> valid = new ArrayList<String>();
                    for (int i = 0; i < ids.length(); i++) {
                        String id = ids.optString(i, "");
                        if (known.contains(id) && !valid.contains(id)) {
                            valid.add(id);
                        }
                    }
                    if (!valid.isEmpty()) {
                        perSlot.put(slotKey, valid);
                    }
                }
                if (!perSlot.isEmpty()) {
                    result.put(focusName, perSlot);
                }
            }
            return result.isEmpty() ? null : result;
        } catch (Exception ignored) {
            return null;
        }
    }

    private void renderProgramDetail() {
        if (program == null) {
            renderTraining();
            return;
        }
        currentTab = "training";
        clear();
        content.addView(title(program.title(), program.level().label() + " · 每周 " + program.daysPerWeek()
                + " 天 · " + program.splitName()));

        LinearLayout overview = card();
        overview.addView(section("每周分化"));
        overview.addView(space(6));
        for (int i = 0; i < program.daysPerWeek(); i++) {
            ProgramFocus focus = program.focusForDay(i);
            overview.addView(text("第 " + (i + 1) + " 练 · " + focus.label() + " —— 覆盖："
                    + join(focus.regions()), 14, Typeface.NORMAL, INK));
        }
        overview.addView(space(8));
        overview.addView(text("动作在生成计划时就按每天的动作模式槽位排好了（蹲/推/拉/髋铰链……），"
                + "并避开前几天已经练过的，所以每天的内容真的不一样。器械和伤痛过滤在排的时候就生效。",
                13, Typeface.NORMAL, MUTED));
        if (schedule != null && !schedule.isEmpty()) {
            overview.addView(space(8));
            overview.addView(button("看训练日历", GREEN, Color.WHITE, v -> renderCalendar()),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        }
        content.addView(overview);

        for (ProgramPhase phase : program.phases()) {
            LinearLayout phaseCard = card();
            phaseCard.addView(text(phase.name() + " · " + phase.weeksLabel(), 17, Typeface.BOLD, INK));
            phaseCard.addView(space(4));
            phaseCard.addView(text("力量课处方：" + phase.prescription().compactLabel(), 14, Typeface.BOLD, BLUE));
            if (phase.aerobicMinutesPerWeek() > 0) {
                phaseCard.addView(text("有氧：每周约 " + phase.aerobicMinutesPerWeek() + " 分钟 · "
                        + phase.aerobicNote(), 13, Typeface.NORMAL, MUTED));
            } else {
                phaseCard.addView(text("有氧：" + phase.aerobicNote(), 13, Typeface.NORMAL, MUTED));
            }
            phaseCard.addView(space(4));
            phaseCard.addView(text(phase.description(), 13, Typeface.NORMAL, MUTED));
            content.addView(phaseCard);
        }

        LinearLayout progression = card();
        progression.addView(section("怎么进阶"));
        progression.addView(space(4));
        progression.addView(text(program.progressionRule(), 14, Typeface.NORMAL, INK));
        content.addView(progression);

        LinearLayout refs = card();
        refs.addView(section("科学依据"));
        refs.addView(space(4));
        for (String ref : program.refs()) {
            refs.addView(text("· " + ref, 12, Typeface.NORMAL, MUTED));
            refs.addView(space(4));
        }
        content.addView(refs);

        LinearLayout actions = card();
        actions.addView(button("返回训练页", GREEN, Color.WHITE, v -> renderTraining()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));
        actions.addView(space(8));
        actions.addView(button("放弃这个计划", Color.rgb(236, 240, 234), CORAL, v ->
                new AlertDialog.Builder(this)
                        .setTitle("放弃当前周期计划？")
                        .setMessage("已完成的训练记录会保留，只清除计划与进度。")
                        .setNegativeButton("取消", null)
                        .setPositiveButton("放弃", (dialog, which) -> {
                            program = null;
                            schedule = null;
                            programWeekdays.clear();
                            pendingProgramKey = "";
                            saveState();
                            renderTraining();
                        })
                        .show()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        content.addView(actions);
        renderBottomNav();
    }

    // ================================================================= 训练日历

    private SessionTimeModel timeModel() {
        return new SessionTimeModel(paceFactor);
    }

    private long todayEpochDay() {
        return LocalDate.now().toEpochDay();
    }

    private String dateLabel(long epochDay) {
        LocalDate date = LocalDate.ofEpochDay(epochDay);
        return date.getMonthValue() + " 月 " + date.getDayOfMonth() + " 日 · "
                + WEEKDAY_LABELS[date.getDayOfWeek().getValue() - 1];
    }

    /** 生成计划时用的推荐输入：伤痛和器械过滤在本机做，AI 只在过滤后的候选里挑。 */
    private RecommendationInput programInput(ProgramPhase phase, ProgramFocus focus) {
        RecommendationInput.Builder builder = new RecommendationInput.Builder()
                .intentText(focus.intentText())
                .intensity(phase.intensity())
                .includeUserUnverified(false)
                .favoriteExercises(favoriteIds)
                .verifiedExercises(reviewedIdsForRecommendation())
                .paceFactor(paceFactor);
        for (String item : equipment) {
            builder.equipment(item);
        }
        addPain(builder, shoulderPain, "shoulder");
        addPain(builder, lowerBackPain, "lower_back");
        addPain(builder, kneePain, "knee");
        return builder.build();
    }

    /**
     * 每天排几个动作：由阶段处方和可用时间反解，而不是查表。
     * 处方是周期计划定的科学约束不能改，能动的只有动作数量。
     * 下限至少覆盖这一天分化声明的所有动作模式——蹲/推/拉这些槽位不能因为强度档的上限被砍掉。
     */
    private int exerciseCountFor(ProgramPhase phase, ProgramFocus focus) {
        int budget = program != null && program.level() == TrainingLevel.BEGINNER ? 35 : 50;
        int floor = Math.max(3, focus.patterns().size());
        int ceiling = Math.max(floor, phase.intensity().maxExercises());
        return timeModel().fitExerciseCount(budget, phase.prescription(), floor, ceiling);
    }

    /** 一次性把 8 周的每一天都排好动作：日历要有内容，跨天去重也只有全局排才做得到。 */
    private ProgramSchedule buildSchedule(final TrainingProgram target, long startEpochDay,
            List<Integer> weekdays) {
        return ProgramSchedule.build(target, startEpochDay, weekdays,
                new ProgramSchedule.DayComposer() {
                    @Override
                    public ProgramComposer.ComposedDay compose(int week, int dayIndex,
                            ProgramFocus focus, ProgramPhase phase, List<String> recentIds) {
                        RecommendationInput input = programInput(phase, focus);
                        return ProgramComposer.composeDay(focus, phase.prescription(),
                                engine().safeCandidates(input), exerciseCountFor(phase, focus),
                                recentIds, favoriteIds);
                    }
                });
    }

    /** 过期未练的标记为漏练（不顺延），返回是否有变化。 */
    private boolean refreshScheduleStatus() {
        if (schedule == null || schedule.isEmpty()) {
            return false;
        }
        ProgramSchedule updated = schedule.markMissedBefore(todayEpochDay());
        boolean changed = false;
        for (int i = 0; i < updated.sessions().size(); i++) {
            if (updated.sessions().get(i).status() != schedule.sessions().get(i).status()) {
                changed = true;
                break;
            }
        }
        schedule = updated;
        return changed;
    }

    private void markScheduledSessionDone(String key) {
        if (schedule == null) {
            return;
        }
        ScheduledSession session = schedule.byKey(key);
        if (session != null) {
            schedule = schedule.withSession(session.withStatus(ScheduledSession.Status.DONE));
        }
    }

    /** 从日历上某一天开练：动作是生成计划时排好的，处方来自该周所在阶段。 */
    private void startScheduledSession(ScheduledSession session) {
        if (inSession) { renderSession(); return; }
        planGeneration++;
        planBudgetMinutes = 0;
        if (program == null || session == null) {
            return;
        }
        ProgramPhase phase = program.phaseForWeek(session.week());
        RecommendationInput input = programInput(phase, session.focus());
        lastInput = input;

        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        for (int i = 0; i < session.exerciseIds().size(); i++) {
            Exercise exercise = exerciseById(session.exerciseIds().get(i));
            if (exercise == null) {
                continue;
            }
            ProgramComposer.Slot slot = i < session.slotKeys().size()
                    ? ProgramComposer.Slot.parse(session.slotKeys().get(i)) : null;
            items.add(ProgramComposer.toItem(exercise, phase.prescription(), favoriteIds, slot));
        }
        if (items.isEmpty()) {
            Toast.makeText(this, "这一天的动作已失效，请重新生成计划", Toast.LENGTH_LONG).show();
            return;
        }
        if (!checkReviewedSelection(items)) return;

        int minutes = timeModel().sessionMinutes(items);
        String title = "第 " + session.week() + " 周 · " + session.focus().label() + " · " + phase.name();
        String reason = "周期计划第 " + session.week() + " 周（" + phase.name() + "）的 "
                + session.focus().label() + "：按 " + join(session.focus().patterns())
                + " 逐个动作模式排的，避开最近几天练过的动作；本阶段处方 "
                + phase.prescription().compactLabel() + "。" + program.progressionRule();
        WorkoutPlan plan = new WorkoutPlan(title, phase.intensity(), minutes, items, reason,
                new ArrayList<String>(), "训练建议遵循低起点、慢进阶原则；如出现疼痛加重请停止。", false);
        pendingProgramKey = session.key();
        applyPlan(plan, false);
        Toast.makeText(this, "已载入这一天的训练（预计 " + minutes + " 分钟）", Toast.LENGTH_SHORT).show();
    }

    private Exercise exerciseById(String id) {
        for (Exercise exercise : allExercises()) {
            if (exercise.id().equals(id)) {
                return exercise;
            }
        }
        return null;
    }

    private void renderCalendar() {
        if (program == null || schedule == null) {
            renderTraining();
            return;
        }
        currentTab = "training";
        clear();
        refreshScheduleStatus();
        if (calendarAnchorEpochDay <= 0) {
            calendarAnchorEpochDay = todayEpochDay();
        }
        LocalDate anchor = LocalDate.ofEpochDay(calendarAnchorEpochDay);
        content.addView(title("训练日历", program.title() + " · 已完成 "
                + schedule.doneCount() + "/" + schedule.totalCount() + " 次"));

        LinearLayout monthCard = card();
        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.addView(button("‹", Color.rgb(236, 240, 234), INK, v -> {
            calendarAnchorEpochDay = anchor.minusMonths(1).withDayOfMonth(1).toEpochDay();
            renderCalendar();
        }), new LinearLayout.LayoutParams(dp(44), dp(38)));
        TextView monthLabel = text(anchor.getYear() + " 年 " + anchor.getMonthValue() + " 月",
                17, Typeface.BOLD, INK);
        monthLabel.setGravity(Gravity.CENTER);
        header.addView(monthLabel, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        header.addView(button("›", Color.rgb(236, 240, 234), INK, v -> {
            calendarAnchorEpochDay = anchor.plusMonths(1).withDayOfMonth(1).toEpochDay();
            renderCalendar();
        }), new LinearLayout.LayoutParams(dp(44), dp(38)));
        monthCard.addView(header);
        monthCard.addView(space(6));
        monthCard.addView(calendarGrid(anchor));
        monthCard.addView(space(8));
        monthCard.addView(text("● 计划   ✓ 已完成   ✗ 漏练   ○ 跳过", 12, Typeface.NORMAL, MUTED));
        content.addView(monthCard);

        ScheduledSession next = schedule.todayOrNext(todayEpochDay());
        if (next != null) {
            LinearLayout nextCard = card();
            nextCard.addView(smallLabel(next.epochDay() == todayEpochDay() ? "今天" : "下一次"));
            nextCard.addView(text(dateLabel(next.epochDay()) + " · " + next.focus().label(),
                    18, Typeface.BOLD, INK));
            nextCard.addView(space(8));
            nextCard.addView(button("查看并开始", GREEN, Color.WHITE, v -> renderScheduledDay(next.key())),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(48)));
            content.addView(nextCard);
        }

        int repeatWeek = schedule.weekNeedingRepeat(todayEpochDay());
        if (repeatWeek > 0) {
            content.addView(repeatWeekCard(repeatWeek));
        } else if (schedule.shouldSuggestReplan(todayEpochDay())) {
            LinearLayout replan = card();
            replan.addView(noteBox("连续两周完成率都不到一半。与其硬扛，不如把每周天数调低重新生成——"
                    + "能持续做完的计划才有效。", CORAL));
            replan.addView(space(8));
            replan.addView(button("重新生成计划", CORAL, Color.WHITE, v -> renderProgramSetup()),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
            content.addView(replan);
        }

        LinearLayout actions = card();
        actions.addView(button("计划详情", Color.rgb(236, 240, 234), INK, v -> renderProgramDetail()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        actions.addView(space(8));
        actions.addView(button("返回训练页", GREEN, Color.WHITE, v -> renderTraining()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        content.addView(actions);
        renderBottomNav();
    }

    private View repeatWeekCard(final int week) {
        LinearLayout box = card();
        box.addView(noteBox("第 " + week + " 周只完成了 "
                + Math.round(schedule.weekCompletion(week, false) * 100)
                + "%。周期化的强度是按周设计的，漏掉的课不会顺延——建议把这一周原样重做一次，"
                + "后面的安排整体后移一周。", CORAL));
        box.addView(space(8));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(button("重做第 " + week + " 周", CORAL, Color.WHITE, v -> {
            schedule = schedule.repeatWeek(week);
            saveState();
            Toast.makeText(this, "已插入重做的第 " + week + " 周", Toast.LENGTH_SHORT).show();
            renderCalendar();
        }), new LinearLayout.LayoutParams(0, dp(44), 1f));
        row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        row.addView(button("继续往下练", Color.rgb(236, 240, 234), INK, v -> {
            // 用户选择不重做：把该周剩下的漏练标成主动跳过，就不会再提示了。
            ProgramSchedule updated = schedule;
            for (ScheduledSession session : schedule.sessions()) {
                if (session.week() == week && session.status() == ScheduledSession.Status.MISSED) {
                    updated = updated.withSession(
                            session.withStatus(ScheduledSession.Status.SKIPPED));
                }
            }
            schedule = updated;
            saveState();
            renderCalendar();
        }), new LinearLayout.LayoutParams(0, dp(44), 1f));
        box.addView(row);
        return box;
    }

    private View calendarGrid(LocalDate anchor) {
        LinearLayout grid = new LinearLayout(this);
        grid.setOrientation(LinearLayout.VERTICAL);

        LinearLayout weekdayRow = new LinearLayout(this);
        weekdayRow.setOrientation(LinearLayout.HORIZONTAL);
        for (String label : WEEKDAY_SHORT) {
            TextView cell = text(label, 11, Typeface.NORMAL, MUTED);
            cell.setGravity(Gravity.CENTER);
            weekdayRow.addView(cell, new LinearLayout.LayoutParams(0,
                    ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        }
        grid.addView(weekdayRow);
        grid.addView(space(4));

        LocalDate first = anchor.withDayOfMonth(1);
        long gridStart = first.toEpochDay() - (first.getDayOfWeek().getValue() - 1);
        int lastDay = anchor.lengthOfMonth();
        long gridEnd = first.plusDays(lastDay - 1).toEpochDay();
        long cursor = gridStart;
        while (cursor <= gridEnd) {
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            for (int i = 0; i < 7; i++) {
                row.addView(calendarCell(cursor + i, anchor.getMonthValue()),
                        new LinearLayout.LayoutParams(0, dp(52), 1f));
            }
            grid.addView(row);
            cursor += 7;
        }
        return grid;
    }

    private View calendarCell(final long epochDay, int month) {
        LocalDate date = LocalDate.ofEpochDay(epochDay);
        LinearLayout cell = new LinearLayout(this);
        cell.setOrientation(LinearLayout.VERTICAL);
        cell.setGravity(Gravity.CENTER);
        boolean inMonth = date.getMonthValue() == month;
        boolean isToday = epochDay == todayEpochDay();

        List<ScheduledSession> onDay = schedule.onDate(epochDay);
        String mark = "";
        int markColor = MUTED;
        if (!onDay.isEmpty()) {
            ScheduledSession session = onDay.get(0);
            switch (session.status()) {
                case DONE:
                    mark = "✓";
                    markColor = GREEN;
                    break;
                case MISSED:
                    mark = "✗";
                    markColor = CORAL;
                    break;
                case SKIPPED:
                    mark = "○";
                    markColor = MUTED;
                    break;
                default:
                    mark = "●";
                    markColor = BLUE;
                    break;
            }
        }
        TextView day = text(String.valueOf(date.getDayOfMonth()), 14,
                isToday ? Typeface.BOLD : Typeface.NORMAL, inMonth ? INK : LINE);
        day.setGravity(Gravity.CENTER);
        cell.addView(day);
        TextView badge = text(mark, 13, Typeface.BOLD, markColor);
        badge.setGravity(Gravity.CENTER);
        cell.addView(badge);
        if (isToday) {
            cell.setBackground(bg(GREEN_SOFT, dp(9), GREEN, 1));
        }
        if (!onDay.isEmpty()) {
            final String key = onDay.get(0).key();
            cell.setOnClickListener(v -> renderScheduledDay(key));
        }
        return cell;
    }

    /** 日历上某一天的课表：动作、组次、预计时长，可以替换动作或跳过这一天。 */
    private void renderScheduledDay(String key) {
        if (program == null || schedule == null) {
            renderTraining();
            return;
        }
        final ScheduledSession session = schedule.byKey(key);
        if (session == null) {
            renderCalendar();
            return;
        }
        currentTab = "training";
        clear();
        ProgramPhase phase = program.phaseForWeek(session.week());
        List<WorkoutItem> items = scheduledItems(session, phase);
        int minutes = timeModel().sessionMinutes(items);

        content.addView(title(dateLabel(session.epochDay()),
                "第 " + session.week() + " 周 · " + session.focus().label() + " · " + phase.name()));

        LinearLayout head = card();
        head.addView(text("预计主课 " + minutes + " 分钟 · " + items.size() + " 个动作",
                17, Typeface.BOLD, BLUE));
        head.addView(text("另建议热身 " + SessionTimeModel.WARMUP_ADVICE_MINUTES + " 分钟、放松 "
                + SessionTimeModel.COOLDOWN_ADVICE_MINUTES + " 分钟", 13, Typeface.NORMAL, MUTED));
        head.addView(space(6));
        head.addView(text("本阶段处方：" + phase.prescription().compactLabel(), 13, Typeface.BOLD, INK));
        if (phase.aerobicMinutesPerWeek() > 0) {
            head.addView(text("有氧：" + phase.aerobicNote(), 13, Typeface.NORMAL, MUTED));
        }
        head.addView(space(4));
        head.addView(text("状态：" + statusLabel(session.status()), 13, Typeface.BOLD,
                session.status() == ScheduledSession.Status.DONE ? GREEN
                        : session.status() == ScheduledSession.Status.MISSED ? CORAL : MUTED));
        content.addView(head);

        for (int i = 0; i < items.size(); i++) {
            content.addView(scheduledItemCard(session, items.get(i), i));
        }

        LinearLayout actions = card();
        if (session.status() != ScheduledSession.Status.DONE) {
            actions.addView(button("▶ 开始这次训练", GREEN, Color.WHITE,
                            v -> startScheduledSession(schedule.byKey(key))),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(50)));
            actions.addView(space(8));
            actions.addView(button("挪到别的日期", Color.rgb(236, 240, 234), INK,
                            v -> promptMoveSession(key)),
                    new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
            actions.addView(space(8));
            actions.addView(button("跳过这一天", Color.rgb(236, 240, 234), CORAL, v -> {
                schedule = schedule.withSession(
                        schedule.byKey(key).withStatus(ScheduledSession.Status.SKIPPED));
                saveState();
                renderCalendar();
            }), new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
            actions.addView(space(8));
        }
        actions.addView(button("返回日历", Color.rgb(236, 240, 234), INK, v -> renderCalendar()),
                new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(44)));
        content.addView(actions);
        renderBottomNav();
    }

    private String statusLabel(ScheduledSession.Status status) {
        switch (status) {
            case DONE:
                return "已完成";
            case MISSED:
                return "漏练（保持周结构，不顺延）";
            case SKIPPED:
                return "已跳过";
            default:
                return "待完成";
        }
    }

    private List<WorkoutItem> scheduledItems(ScheduledSession session, ProgramPhase phase) {
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        for (int i = 0; i < session.exerciseIds().size(); i++) {
            Exercise exercise = exerciseById(session.exerciseIds().get(i));
            if (exercise == null) {
                continue;
            }
            ProgramComposer.Slot slot = i < session.slotKeys().size()
                    ? ProgramComposer.Slot.parse(session.slotKeys().get(i)) : null;
            items.add(ProgramComposer.toItem(exercise, phase.prescription(), favoriteIds, slot));
        }
        return items;
    }

    private View scheduledItemCard(final ScheduledSession session, WorkoutItem item, final int index) {
        LinearLayout card = card();
        card.addView(mediaStrip(item.exercise()));
        card.addView(space(8));
        card.addView(text((index + 1) + ". " + item.exercise().name(), 17, Typeface.BOLD, INK));
        card.addView(text(reviewLabel(item.exercise()), 12, Typeface.BOLD, isReviewed(item.exercise()) ? GREEN : AMBER));
        card.addView(text(join(item.exercise().targetRegions()) + " · " + item.reason(),
                12, Typeface.NORMAL, MUTED));
        card.addView(space(4));
        card.addView(text(item.prescription().compactLabel(), 14, Typeface.BOLD, BLUE));
        card.addView(text("约 " + Math.max(1, timeModel().itemSeconds(item.prescription()) / 60)
                + " 分钟", 12, Typeface.NORMAL, MUTED));
        card.addView(space(8));
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.addView(button("换动作", BLUE, Color.WHITE,
                        v -> promptReplaceScheduled(session.key(), index)),
                new LinearLayout.LayoutParams(0, dp(40), 1f));
        row.addView(space(10), new LinearLayout.LayoutParams(dp(10), 1));
        row.addView(button("详情", Color.rgb(236, 240, 234), INK,
                        v -> showExerciseDetail(item.exercise())),
                new LinearLayout.LayoutParams(0, dp(40), 1f));
        card.addView(row);
        return card;
    }

    /** 换动作：锁定这个槽位的动作模式，给几个候选让用户自己挑，选完记在那一天。 */
    private void promptReplaceScheduled(final String key, final int index) {
        final ScheduledSession session = schedule.byKey(key);
        if (session == null || index >= session.exerciseIds().size()) {
            return;
        }
        ProgramPhase phase = program.phaseForWeek(session.week());
        ProgramComposer.Slot slot = index < session.slotKeys().size()
                ? ProgramComposer.Slot.parse(session.slotKeys().get(index))
                : ProgramComposer.Slot.region(session.focus().regions().get(0));
        RecommendationInput input = programInput(phase, session.focus());
        Set<String> exclude = new LinkedHashSet<String>(session.exerciseIds());
        final List<Exercise> options = ProgramComposer.candidatesFor(slot, session.focus(),
                engine().safeCandidates(input), exclude, recentExerciseIds(), favoriteIds, 6);
        if (options.isEmpty()) {
            Toast.makeText(this, "当前器械和伤痛设置下没有可替换的动作", Toast.LENGTH_SHORT).show();
            return;
        }
        String[] labels = new String[options.size()];
        for (int i = 0; i < options.size(); i++) {
            labels[i] = options.get(i).name() + "（" + join(options.get(i).targetRegions()) + "）";
        }
        new AlertDialog.Builder(this)
                .setTitle("替换「" + slot.label() + "」槽位")
                .setItems(labels, (dialog, which) -> {
                    ScheduledSession current = schedule.byKey(key);
                    if (current == null) {
                        return;
                    }
                    schedule = schedule.withSession(
                            current.withExerciseAt(index, options.get(which).id()));
                    saveState();
                    renderScheduledDay(key);
                })
                .setNegativeButton("取消", null)
                .show();
    }

    private void promptMoveSession(final String key) {
        final ScheduledSession session = schedule.byKey(key);
        if (session == null) {
            return;
        }
        final int[] offsets = {-2, -1, 1, 2, 3};
        String[] labels = new String[offsets.length];
        for (int i = 0; i < offsets.length; i++) {
            labels[i] = dateLabel(session.epochDay() + offsets[i]);
        }
        new AlertDialog.Builder(this)
                .setTitle("挪到哪一天")
                .setItems(labels, (dialog, which) -> {
                    ScheduledSession current = schedule.byKey(key);
                    if (current == null) {
                        return;
                    }
                    schedule = schedule.withSession(
                            current.withDate(current.epochDay() + offsets[which])
                                    .withStatus(ScheduledSession.Status.PLANNED));
                    saveState();
                    renderCalendar();
                })
                .setNegativeButton("取消", null)
                .show();
    }

    // =========================================================== 临时加练与训练量

    /**
     * 把训练记录还原成结构化的训练量：练了哪些部位、几组、什么时候。
     * 只有带 itemStats 的记录能还原——老记录只有文字行，算不出组数。
     */
    private List<TrainingLoad> trainingLoads(long sinceMillis) {
        List<TrainingLoad> loads = new ArrayList<TrainingLoad>();
        for (SessionRecord record : trainingRecords) {
            if (record.epochMillis < sinceMillis || record.itemStats.isEmpty()) {
                continue;
            }
            for (String stat : record.itemStats) {
                String[] parts = stat.split("\\|");
                if (parts.length < 2) {
                    continue;
                }
                Exercise exercise = exerciseById(parts[0]);
                if (exercise == null) {
                    continue;
                }
                int sets;
                try {
                    sets = Integer.parseInt(parts[1]);
                } catch (NumberFormatException ignored) {
                    continue;
                }
                if (sets > 0) {
                    loads.add(new TrainingLoad(exercise.targetRegions(), sets, record.epochMillis));
                }
            }
        }
        return loads;
    }

    private long startOfThisWeekMillis() {
        return ProgramSchedule.startOfWeek(todayEpochDay()) * 86_400_000L
                - java.util.TimeZone.getDefault().getRawOffset();
    }

    private TrainingLevel currentLevel() {
        return assessment == null ? TrainingLevel.BEGINNER : assessment.level();
    }

    private WeeklyVolumeLedger weeklyLedger() {
        long weekStart = startOfThisWeekMillis();
        return WeeklyVolumeLedger.of(trainingLoads(weekStart), currentLevel(), weekStart);
    }

    private RecoveryState recoveryState() {
        long since = System.currentTimeMillis() - 7 * 24 * 3600_000L;
        return RecoveryState.of(trainingLoads(since), System.currentTimeMillis());
    }

    /** 明天计划课要练的部位——加练要避开，否则明天那节课的质量会崩。 */
    private Set<String> tomorrowPlannedRegions() {
        Set<String> regions = new LinkedHashSet<String>();
        if (schedule == null) {
            return regions;
        }
        for (ScheduledSession session : schedule.onDate(todayEpochDay() + 1)) {
            if (session.status() != ScheduledSession.Status.PLANNED) {
                continue;
            }
            for (String id : session.exerciseIds()) {
                Exercise exercise = exerciseById(id);
                if (exercise != null) {
                    regions.addAll(exercise.targetRegions());
                }
            }
        }
        return regions;
    }

    /** 最近练过的动作 id，按时间倒序（记录 + 计划两边都算）。 */
    private List<String> recentlyTrainedExerciseIds() {
        List<String> ids = new ArrayList<String>();
        for (SessionRecord record : trainingRecords) {
            if (ids.size() >= 24) {
                break;
            }
            for (String stat : record.itemStats) {
                String id = stat.split("\\|")[0];
                if (id.length() > 0 && !ids.contains(id)) {
                    ids.add(id);
                }
            }
        }
        return ids;
    }

    /** 最近生成 + 最近完成合并去重；它只影响同类动作排序，不绕过安全或器械过滤。 */
    private List<String> recentExerciseIdsForRecommendation() {
        LinkedHashSet<String> merged = new LinkedHashSet<String>();
        merged.addAll(recentRecommendationIds);
        merged.addAll(recentlyTrainedExerciseIds());
        List<String> result = new ArrayList<String>();
        for (String id : merged) {
            if (result.size() >= 24) break;
            result.add(id);
        }
        return result;
    }

    private void rememberRecommendedPlan(WorkoutPlan plan) {
        if (plan == null || plan.items().isEmpty()) return;
        for (int i = plan.items().size() - 1; i >= 0; i--) {
            String id = plan.items().get(i).exercise().id();
            recentRecommendationIds.remove(id);
            recentRecommendationIds.add(0, id);
        }
        while (recentRecommendationIds.size() > 24) {
            recentRecommendationIds.remove(recentRecommendationIds.size() - 1);
        }
        getSharedPreferences("fitness_state", MODE_PRIVATE).edit()
                .putString("recentRecommendationsV1", new JSONArray(recentRecommendationIds).toString())
                .apply();
    }

    /** 生成一次临时加练：时长是硬约束，动作数和组数是解出来的。 */
    private void generateAdHocSession(String rawText, boolean unknown) {
        if (inSession) { renderSession(); return; }
        planGeneration++;
        Intensity requestedIntensity = selectedIntensity;
        Intensity effectiveIntensity = allowedDailyIntensity(requestedIntensity);
        pendingProgramKey = "";
        AdHocIntent intent = AdHocIntent.parse(unknown ? "" : rawText);
        planBudgetMinutes = intent.minutes() > 0 ? intent.minutes()
                : selectedDurationMinutes > 0 ? selectedDurationMinutes : 20;
        RecommendationInput input = adHocInput(rawText, unknown, intent, effectiveIntensity);
        lastInput = input;

        WeeklyVolumeLedger ledger = weeklyLedger();
        AdHocPlanner.Request request = new AdHocPlanner.Request()
                .intent(intent)
                .minutes(selectedDurationMinutes > 0 ? selectedDurationMinutes : 20)
                .intensity(effectiveIntensity)
                .level(currentLevel())
                .paceFactor(paceFactor)
                .recovery(recoveryState())
                .ledger(ledger)
                .tomorrowRegions(tomorrowPlannedRegions())
                .favoriteIds(favoriteIds)
                .recentExerciseIds(recentExerciseIdsForRecommendation());

        WorkoutPlan plan = explainDailyIntensity(AdHocPlanner.plan(engine().safeCandidates(input), request), requestedIntensity);
        if (plan.items().isEmpty()) {
            applyGeneratedPlan(plan, false);
            Toast.makeText(this, "当前器械/伤痛/排除条件下没有可用动作，请调整后再试", Toast.LENGTH_LONG).show();
            return;
        }
        if (aiConfigured()) {
            generateTrainingWithAi(plan, rawText, unknown);
            return;
        }
        applyGeneratedPlan(plan, false);
        Toast.makeText(this, "已生成加练：" + plan.items().size() + " 个动作 · 预计 "
                + plan.estimatedMinutes() + " 分钟", Toast.LENGTH_SHORT).show();
    }

    /** 加练的推荐输入：意图里说了排除部位就带进去，安全/器械过滤仍走推荐引擎。 */
    private RecommendationInput adHocInput(String rawText, boolean unknown, AdHocIntent intent, Intensity effectiveIntensity) {
        RecommendationInput.Builder builder = new RecommendationInput.Builder()
                .intentText(unknown ? "" : rawText)
                .intensity(effectiveIntensity)
                .targetMinutes(intent.minutes() > 0 ? intent.minutes() : selectedDurationMinutes)
                .includeUserUnverified(false)
                .favoriteExercises(favoriteIds)
                .verifiedExercises(reviewedIdsForRecommendation())
                .paceFactor(paceFactor)
                .recentExerciseIds(recentExerciseIdsForRecommendation());
        if (unknown) {
            builder.unknownWorkout();
        }
        for (String item : equipment) {
            builder.equipment(item);
        }
        addPain(builder, shoulderPain, "shoulder");
        addPain(builder, lowerBackPain, "lower_back");
        addPain(builder, kneePain, "knee");
        return builder.build();
    }

    /** 本周各肌群做了多少组——把计划课和加练放进同一本账。 */
    private View weeklyVolumeCard() {
        WeeklyVolumeLedger ledger = weeklyLedger();
        boolean anyVolume = false;
        for (WeeklyVolumeLedger.Entry entry : ledger.entries()) {
            anyVolume = anyVolume || entry.sets() > 0;
        }
        if (!anyVolume) {
            return null;
        }
        LinearLayout card = card();
        card.addView(section("本周训练量"));
        card.addView(space(6));
        for (WeeklyVolumeLedger.Entry entry : ledger.entries()) {
            if (entry.sets() <= 0 && entry.status() != WeeklyVolumeLedger.Status.LOW) {
                continue;
            }
            int color = entry.status() == WeeklyVolumeLedger.Status.HIGH ? CORAL
                    : entry.status() == WeeklyVolumeLedger.Status.OK ? GREEN : MUTED;
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            TextView label = text(entry.label(), 13, Typeface.NORMAL, color);
            row.addView(label, new LinearLayout.LayoutParams(0,
                    ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            row.addView(text(entry.status() == WeeklyVolumeLedger.Status.HIGH ? "偏多"
                            : entry.status() == WeeklyVolumeLedger.Status.OK ? "合适" : "还差",
                    12, Typeface.BOLD, color));
            card.addView(row);
            card.addView(space(3));
        }
        card.addView(space(4));
        card.addView(text("主要部位记 1 组、间接参与记 0.5 组；计划课和加练算同一本账。"
                + GuidelineRefs.VOLUME_DOSE_RESPONSE, 11, Typeface.NORMAL, MUTED));
        return card;
    }

    /** 最近练过的动作 id，按时间倒序——用来避开刚练过的动作。 */
    private List<String> recentExerciseIds() {
        List<String> ids = new ArrayList<String>();
        if (schedule == null) {
            return ids;
        }
        List<ScheduledSession> done = new ArrayList<ScheduledSession>();
        for (ScheduledSession session : schedule.sessions()) {
            if (session.status() == ScheduledSession.Status.DONE) {
                done.add(session);
            }
        }
        for (int i = done.size() - 1; i >= 0 && ids.size() < 24; i--) {
            for (String id : done.get(i).exerciseIds()) {
                if (!ids.contains(id)) {
                    ids.add(id);
                }
            }
        }
        return ids;
    }

    private void renderBottomNav() {
        bottomNav.removeAllViews();
        navItem("今天", "training", R.drawable.ic_nav_train, v -> renderTraining());
        navItem("动作库", "library", R.drawable.ic_nav_library, v -> renderLibrary(libraryFilter));
        navItem("记录", "records", R.drawable.ic_nav_records, v -> renderRecords());
        navItem("吃什么", "food", R.drawable.ic_nav_food, v -> renderFood());
    }

    private void navItem(String label, String tab, int iconRes, View.OnClickListener listener) {
        boolean active = currentTab.equals(tab);
        LinearLayout item = new LinearLayout(this);
        item.setOrientation(LinearLayout.VERTICAL);
        item.setGravity(Gravity.CENTER);
        item.setPadding(dp(4), dp(7), dp(4), dp(6));
        if (active) {
            item.setBackground(bg(GREEN_SOFT, dp(14), GREEN_SOFT, 0));
        }
        ImageView icon = new ImageView(this);
        icon.setImageResource(iconRes);
        icon.setColorFilter(active ? GREEN : MUTED);
        item.addView(icon, new LinearLayout.LayoutParams(dp(22), dp(22)));
        TextView label2 = text(label, 11, active ? Typeface.BOLD : Typeface.NORMAL, active ? GREEN : MUTED);
        label2.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams labelLp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        labelLp.setMargins(0, dp(3), 0, 0);
        item.addView(label2, labelLp);
        item.setOnClickListener(v -> {
            if (inSession) pauseWorkout();
            listener.onClick(v);
        });
        LinearLayout.LayoutParams itemLp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        itemLp.setMargins(dp(5), 0, dp(5), 0);
        bottomNav.addView(item, itemLp);
    }

    private LinearLayout title(String title, String subtitle) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(0, 0, 0, dp(12));

        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.ic_logo_badge);
        LinearLayout.LayoutParams logoLp = new LinearLayout.LayoutParams(dp(46), dp(46));
        logoLp.setMargins(0, 0, dp(12), 0);
        row.addView(logo, logoLp);

        LinearLayout texts = new LinearLayout(this);
        texts.setOrientation(LinearLayout.VERTICAL);
        texts.addView(text(title, 26, Typeface.BOLD, INK));
        texts.addView(text(subtitle, 13, Typeface.NORMAL, MUTED));
        row.addView(texts, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        if (!inSession && !"settings".equals(currentTab)) {
            ImageView gear = new ImageView(this);
            gear.setImageResource(R.drawable.ic_nav_settings);
            gear.setColorFilter(MUTED);
            gear.setBackground(bg(SURFACE, dp(12), LINE, 1));
            gear.setPadding(dp(9), dp(9), dp(9), dp(9));
            gear.setContentDescription("设置");
            gear.setOnClickListener(v -> renderSettings());
            LinearLayout.LayoutParams gearLp = new LinearLayout.LayoutParams(dp(40), dp(40));
            gearLp.setMargins(dp(8), 0, 0, 0);
            row.addView(gear, gearLp);
        }
        return row;
    }

    private LinearLayout card() {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(dp(16), dp(16), dp(16), dp(16));
        card.setBackground(bg(SURFACE, dp(16), SURFACE, 0));
        card.setElevation(dp(3));
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        params.setMargins(dp(2), dp(7), dp(2), dp(9));
        card.setLayoutParams(params);
        return card;
    }

    private String effectiveMedia(Exercise exercise) {
        if (mediaOverrides.containsKey(exercise.id())) {
            return mediaOverrides.get(exercise.id());
        }
        return exercise.media();
    }

    private boolean hasEffectiveMedia(Exercise exercise) {
        String media = effectiveMedia(exercise);
        return media != null && media.length() > 0;
    }

    private View mediaStrip(final Exercise exercise) {
        return mediaStrip(exercise, true);
    }

    private View mediaStrip(final Exercise exercise, boolean clickable) {
        FrameLayout frame = new FrameLayout(this);
        frame.setBackground(bg(Color.WHITE, dp(8), Color.rgb(235, 239, 232), 1));
        frame.setLayoutParams(new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(160)));
        final int radius = dp(8);
        frame.setClipToOutline(true);
        frame.setOutlineProvider(new ViewOutlineProvider() {
            @Override
            public void getOutline(View view, Outline outline) {
                outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), radius);
            }
        });

        String media = effectiveMedia(exercise);
        boolean localReadable = !isLocalUri(media) || canReadLocalMedia(media);
        boolean imageLike = hasEffectiveMedia(exercise)
                && localReadable
                && (isPackagedMedia(media) || isLocalUri(media) || (isWebUrl(media) && isImageUrl(media)));
        if (imageLike) {
            ImageView image = new ImageView(this);
            image.setScaleType(ImageView.ScaleType.FIT_CENTER);
            frame.addView(image, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
            if (isPackagedMedia(media)) {
                loadPackagedImage(image, media, 480, true);
            } else {
                loadThumbInto(image, media);
            }
        } else {
            String label = hasEffectiveMedia(exercise) && isLocalUri(media) && !localReadable
                    ? "本地示范已失效\n点此重新选择"
                    : hasEffectiveMedia(exercise) ? "打开动作来源" : "暂无动作示范\n请查看下方文字要点";
            TextView placeholder = text(label, 15, Typeface.NORMAL, MUTED);
            placeholder.setGravity(Gravity.CENTER);
            frame.addView(placeholder, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        }

        TextView tag = text(exercise.targetRegions().isEmpty() ? "动作" : exercise.targetRegions().get(0),
                12, Typeface.BOLD, GREEN);
        tag.setPadding(dp(7), dp(3), dp(7), dp(3));
        tag.setBackground(bg(GREEN_SOFT, dp(7), GREEN_SOFT, 0));
        FrameLayout.LayoutParams tagLp = new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        tagLp.gravity = Gravity.TOP | Gravity.LEFT;
        tagLp.setMargins(dp(10), dp(8), 0, 0);
        frame.addView(tag, tagLp);

        if (clickable) {
            frame.setOnClickListener(v -> openMedia(exercise));
        }
        return frame;
    }

    private View regionIllustration(final Exercise exercise) {
        final int tile = regionIllustrationTile(exercise);
        return new View(this) {
            private final Paint illustrationPaint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.FILTER_BITMAP_FLAG);

            @Override
            protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                Bitmap sprite = regionSprite();
                if (sprite == null) {
                    canvas.drawColor(regionColor(exercise));
                    return;
                }
                int cellWidth = sprite.getWidth() / 3;
                int cellHeight = sprite.getHeight() / 3;
                int column = tile % 3;
                int row = tile / 3;
                Rect source = new Rect(column * cellWidth, row * cellHeight,
                        (column + 1) * cellWidth, (row + 1) * cellHeight);
                canvas.drawColor(Color.rgb(250, 248, 242));
                float scale = Math.min(getWidth() / (float) cellWidth, getHeight() / (float) cellHeight);
                int targetWidth = Math.round(cellWidth * scale);
                int targetHeight = Math.round(cellHeight * scale);
                int left = (getWidth() - targetWidth) / 2;
                int top = (getHeight() - targetHeight) / 2;
                Rect target = new Rect(left, top, left + targetWidth, top + targetHeight);
                canvas.drawBitmap(sprite, source, target, illustrationPaint);
            }
        };
    }

    private Bitmap regionSprite() {
        if (regionSpriteBitmap == null || regionSpriteBitmap.isRecycled()) {
            regionSpriteBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.exercise_region_sprite);
        }
        return regionSpriteBitmap;
    }

    private int regionIllustrationTile(Exercise exercise) {
        List<String> regions = exercise.targetRegions();
        if (regions.contains("臀")) return 3;
        if (regions.contains("背")) return 0;
        if (regions.contains("胸")) return 1;
        if (regions.contains("腿")) return 2;
        if (regions.contains("肩")) return 4;
        if (regions.contains("核心")) return 5;
        if (regions.contains("手臂")) return 6;
        if (regions.contains("有氧")) return 7;
        if (regions.contains("颈")) return 8;
        return 7;
    }

    private int regionColor(Exercise exercise) {
        List<String> regions = exercise.targetRegions();
        if (regions.contains("背")) {
            return GREEN;
        }
        if (regions.contains("胸")) {
            return CORAL;
        }
        if (regions.contains("腿") || regions.contains("臀")) {
            return AMBER;
        }
        if (regions.contains("肩")) {
            return BLUE;
        }
        if (regions.contains("核心")) {
            return Color.rgb(85, 118, 130);
        }
        if (regions.contains("手臂")) {
            return Color.rgb(120, 110, 150);
        }
        // custom groups (e.g. 瑜伽) get a stable color from a small palette
        String key = regions.isEmpty() ? "" : regions.get(0);
        int[] palette = {
                Color.rgb(126, 102, 168),
                Color.rgb(58, 130, 150),
                Color.rgb(165, 116, 80),
                Color.rgb(90, 140, 110)
        };
        return palette[Math.abs(key.hashCode()) % palette.length];
    }

    private int darken(int color) {
        float f = 0.74f;
        return Color.rgb((int) (Color.red(color) * f), (int) (Color.green(color) * f), (int) (Color.blue(color) * f));
    }

    private void openMedia(Exercise exercise) {
        if (hasEffectiveMedia(exercise)) {
            showMediaPlayer(exercise);
        } else {
            showExerciseDetail(exercise);
        }
    }

    private void showMediaPlayer(final Exercise exercise) {
        final String url = effectiveMedia(exercise);
        final WebView[] webRef = new WebView[1];
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(8), dp(8), dp(8), dp(8));
        boolean shown = false;
        if (isPackagedMedia(url)) {
            ImageView image = new ImageView(this);
            image.setScaleType(ImageView.ScaleType.FIT_CENTER);
            if (loadPackagedImage(image, url)) {
                box.addView(roundedMedia(image, dp(260)));
                shown = true;
            }
        } else if (isLocalUri(url)) {
            ImageView image = new ImageView(this);
            image.setAdjustViewBounds(true);
            if (loadLocalImage(image, url)) {
                box.addView(roundedMedia(image, dp(260)));
                shown = true;
            }
        } else if (isWebUrl(url) && isImageUrl(url)) {
            WebView web = new WebView(this);
            web.getSettings().setLoadWithOverviewMode(true);
            web.getSettings().setUseWideViewPort(true);
            web.getSettings().setBuiltInZoomControls(true);
            web.getSettings().setDisplayZoomControls(false);
            String safe = url.replace("'", "%27");
            String second = twoFrameSibling(url);
            String html;
            if (second != null) {
                web.getSettings().setJavaScriptEnabled(true);
                html = "<html><body style='margin:0;background:#000;display:flex;align-items:center;"
                        + "justify-content:center;height:100vh'>"
                        + "<img id='f' src='" + safe + "' style='max-width:100%;max-height:100%'/>"
                        + "<script>var a='" + safe + "',b='" + second.replace("'", "%27") + "',c=0;"
                        + "setInterval(function(){c=1-c;document.getElementById('f').src=c?b:a;},800);</script>"
                        + "</body></html>";
            } else {
                html = "<html><body style='margin:0;background:#000;text-align:center'>"
                        + "<img src='" + safe + "' style='max-width:100%;height:auto'/></body></html>";
            }
            web.loadDataWithBaseURL(null, html, "text/html", "utf-8", null);
            box.addView(web, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(240)));
            webRef[0] = web;
            shown = true;
        }
        if (!shown) {
            if (isLocalUri(url)) {
                box.addView(text("这张本地示范已失效，常见原因是旧版只保存了相册临时地址。",
                        14, Typeface.BOLD, CORAL));
                box.addView(space(6));
                box.addView(text("请重新选择原图片或 GIF。新版会复制到 App 内保存，重启后仍可显示。",
                        13, Typeface.NORMAL, MUTED));
            } else if (isWebUrl(url)) {
                box.addView(text("该动作的示范是一个网页链接：", 14, Typeface.NORMAL, INK));
                box.addView(space(6));
                box.addView(text(url, 13, Typeface.NORMAL, BLUE));
                box.addView(space(6));
                box.addView(text("点“在浏览器打开”查看示范图或视频。", 13, Typeface.NORMAL, MUTED));
            } else {
                box.addView(text("暂无可用的动作示范，请在编辑中重新选择图片或 GIF。",
                        14, Typeface.NORMAL, MUTED));
            }
        }
        AlertDialog.Builder builder = new AlertDialog.Builder(this)
                .setTitle(exercise.name() + " · 示范")
                .setView(box)
                .setNegativeButton("关闭", null);
        if (isWebUrl(url)) {
            builder.setPositiveButton("在浏览器打开", (dialog, which) -> openExternal(url));
        } else if (isLocalUri(url) && !shown) {
            builder.setPositiveButton("重新选择", (dialog, which) -> editExercise(exercise));
        }
        AlertDialog dialog = builder.create();
        dialog.setOnDismissListener(d -> {
            if (webRef[0] != null) {
                webRef[0].destroy();
            }
        });
        dialog.show();
    }

    private View buildMediaView(final Exercise exercise, int heightPx, WebView[] webRef) {
        String url = effectiveMedia(exercise);
        if (hasEffectiveMedia(exercise) && isPackagedMedia(url)) {
            ImageView image = new ImageView(this);
            image.setScaleType(ImageView.ScaleType.FIT_CENTER);
            if (loadPackagedImage(image, url)) {
                return roundedMedia(image, heightPx);
            }
        } else if (hasEffectiveMedia(exercise) && isLocalUri(url)) {
            ImageView image = new ImageView(this);
            image.setScaleType(ImageView.ScaleType.FIT_CENTER);
            if (loadLocalImage(image, url)) {
                return roundedMedia(image, heightPx);
            }
            TextView missing = text("本地示范已失效\n点此重新选择", 15, Typeface.BOLD, CORAL);
            missing.setGravity(Gravity.CENTER);
            missing.setBackground(bg(Color.rgb(252, 244, 240), dp(10), LINE, 1));
            missing.setOnClickListener(v -> showMediaPlayer(exercise));
            missing.setLayoutParams(new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, heightPx));
            return missing;
        } else if (hasEffectiveMedia(exercise) && isWebUrl(url) && isImageUrl(url)) {
            WebView web = new WebView(this);
            web.getSettings().setLoadWithOverviewMode(true);
            web.getSettings().setUseWideViewPort(true);
            String safe = url.replace("'", "%27");
            String second = twoFrameSibling(url);
            String html;
            if (second != null) {
                web.getSettings().setJavaScriptEnabled(true);
                html = "<html><body style='margin:0;background:#000;display:flex;align-items:center;"
                        + "justify-content:center;height:100vh'>"
                        + "<img id='f' src='" + safe + "' style='max-width:100%;max-height:100%'/>"
                        + "<script>var a='" + safe + "',b='" + second.replace("'", "%27") + "',c=0;"
                        + "setInterval(function(){c=1-c;document.getElementById('f').src=c?b:a;},800);</script>"
                        + "</body></html>";
            } else {
                html = "<html><body style='margin:0;background:#000;text-align:center'>"
                        + "<img src='" + safe + "' style='max-width:100%;height:auto'/></body></html>";
            }
            web.loadDataWithBaseURL(null, html, "text/html", "utf-8", null);
            if (webRef != null) {
                webRef[0] = web;
            }
            return roundedMedia(web, heightPx);
        }
        return mediaStrip(exercise, true);
    }

    private boolean isPackagedMedia(String value) {
        return value != null && value.startsWith("raw:");
    }

    private boolean loadPackagedImage(ImageView image, String value) {
        return loadPackagedImage(image, value, 480, false);
    }

    private boolean loadPackagedImage(ImageView image, String value, int maxEdge, boolean preview) {
        int resId = packagedMediaResId(value);
        if (resId == 0) {
            return false;
        }
        try {
            if (Build.VERSION.SDK_INT >= 28) {
                ImageDecoder.Source source = ImageDecoder.createSource(getResources(), resId);
                Drawable drawable = ImageDecoder.decodeDrawable(source, (decoder, info, src) -> {
                    int width = info.getSize().getWidth(), height = info.getSize().getHeight();
                    float scale = Math.min(1f, maxEdge / (float) Math.max(width, height));
                    decoder.setTargetSize(Math.max(1, Math.round(width * scale)), Math.max(1, Math.round(height * scale)));
                });
                image.setImageDrawable(drawable);
                if (preview) startVisiblePreview(image, drawable); else startAnimatedDrawable(image, drawable);
            } else {
                Drawable movieDrawable = loadMovieDrawable(resId);
                if (movieDrawable == null) {
                    return false;
                }
                image.setImageDrawable(movieDrawable);
                ((MovieDrawable) movieDrawable).start();
            }
            return true;
        } catch (Exception ignored) {
            return false;
        }
    }

    /** Dynamic covers keep playing while visible; offscreen previews do not consume frame work. */
    private void startVisiblePreview(ImageView image, Drawable drawable) {
        image.setContentDescription("动态封面，点开查看示范");
        if (!(drawable instanceof AnimatedImageDrawable)) return;
        AnimatedImageDrawable animated = (AnimatedImageDrawable) drawable;
        animated.setRepeatCount(AnimatedImageDrawable.REPEAT_INFINITE);
        Runnable update = () -> {
            Rect visible = new Rect();
            if (image.isAttachedToWindow() && image.hasWindowFocus() && image.isShown() && image.getGlobalVisibleRect(visible)) animated.start();
            else animated.stop();
        };
        android.view.ViewTreeObserver.OnScrollChangedListener scroll = update::run;
        android.view.ViewTreeObserver.OnWindowFocusChangeListener window = focus -> update.run();
        image.addOnAttachStateChangeListener(new View.OnAttachStateChangeListener() {
            @Override public void onViewAttachedToWindow(View v) {
                image.getViewTreeObserver().addOnScrollChangedListener(scroll);
                image.getViewTreeObserver().addOnWindowFocusChangeListener(window);
                image.post(update);
            }
            @Override public void onViewDetachedFromWindow(View v) {
                animated.stop(); image.removeCallbacks(update);
                if (image.getViewTreeObserver().isAlive()) {
                    image.getViewTreeObserver().removeOnScrollChangedListener(scroll);
                    image.getViewTreeObserver().removeOnWindowFocusChangeListener(window);
                }
            }
        });
    }

    private Drawable loadMovieDrawable(int resId) {
        try {
            Movie movie = Movie.decodeStream(getResources().openRawResource(resId));
            return movie == null ? null : new MovieDrawable(movie);
        } catch (Exception ignored) {
            return null;
        }
    }

    private int packagedMediaResId(String value) {
        if (!isPackagedMedia(value)) {
            return 0;
        }
        String name = value.substring("raw:".length()).trim();
        if (name.length() == 0) {
            return 0;
        }
        return getResources().getIdentifier(name, "raw", getPackageName());
    }

    private View roundedMedia(View inner, int heightPx) {
        FrameLayout frame = new FrameLayout(this);
        final int radius = dp(10);
        frame.setBackgroundColor(BG);
        frame.setClipToOutline(true);
        frame.setOutlineProvider(new ViewOutlineProvider() {
            @Override
            public void getOutline(View view, Outline outline) {
                outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), radius);
            }
        });
        frame.addView(inner, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        frame.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, heightPx));
        if (inner instanceof ImageView && ((ImageView) inner).getDrawable() instanceof AnimatedImageDrawable) {
            AnimatedImageDrawable animated = (AnimatedImageDrawable) ((ImageView) inner).getDrawable();
            LinearLayout controls = new LinearLayout(this); controls.setOrientation(LinearLayout.VERTICAL);
            controls.addView(frame);
            Button pause = button("暂停示范", GREEN_SOFT, GREEN, v -> {});
            pause.setOnClickListener(v -> {
                if (animated.isRunning()) { animated.stop(); pause.setText("播放示范"); }
                else { animated.start(); pause.setText("暂停示范"); }
            });
            controls.addView(pause, fullButton());
            controls.addView(text("阶段图会分步切换；可暂停查看姿势。", 12, Typeface.NORMAL, MUTED));
            return controls;
        }
        return frame;
    }

    private boolean isLocalUri(String value) {
        return value != null && (value.startsWith("content://") || value.startsWith("file://"));
    }

    private String twoFrameSibling(String url) {
        if (url != null && url.contains("free-exercise-db") && url.endsWith("/0.jpg")) {
            return url.substring(0, url.length() - "0.jpg".length()) + "1.jpg";
        }
        return null;
    }

    private boolean loadLocalImage(ImageView image, String url) {
        try {
            Uri uri = Uri.parse(url);
            if (Build.VERSION.SDK_INT >= 28) {
                ImageDecoder.Source source = "file".equalsIgnoreCase(uri.getScheme())
                        ? ImageDecoder.createSource(new File(uri.getPath()))
                        : ImageDecoder.createSource(getContentResolver(), uri);
                Drawable drawable = ImageDecoder.decodeDrawable(source);
                image.setImageDrawable(drawable);
                startAnimatedDrawable(image, drawable);
            } else {
                image.setImageURI(uri);
            }
            return true;
        } catch (Exception ignored) {
            return false;
        }
    }

    private InputStream openLocalMedia(Uri uri) throws java.io.IOException {
        if (uri != null && "file".equalsIgnoreCase(uri.getScheme())) {
            String path = uri.getPath();
            if (path == null) throw new java.io.IOException("Missing local path");
            return new FileInputStream(new File(path));
        }
        return getContentResolver().openInputStream(uri);
    }

    private boolean canReadLocalMedia(String value) {
        if (!isLocalUri(value)) return false;
        InputStream input = null;
        try {
            input = openLocalMedia(Uri.parse(value));
            return input != null && input.read() != -1;
        } catch (Exception ignored) {
            return false;
        } finally {
            if (input != null) try { input.close(); } catch (Exception ignored) {}
        }
    }

    private void startAnimatedDrawable(ImageView image, Drawable drawable) {
        if (Build.VERSION.SDK_INT >= 28 && drawable instanceof AnimatedImageDrawable) {
            AnimatedImageDrawable animated = (AnimatedImageDrawable) drawable;
            animated.setRepeatCount(AnimatedImageDrawable.REPEAT_INFINITE);
            image.addOnAttachStateChangeListener(new View.OnAttachStateChangeListener() {
                @Override public void onViewAttachedToWindow(View v) { animated.start(); }
                @Override public void onViewDetachedFromWindow(View v) { animated.stop(); }
            });
            animated.start();
        }
    }

    private static class MovieDrawable extends Drawable implements android.graphics.drawable.Animatable {
        private final Movie movie;
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.FILTER_BITMAP_FLAG);
        private final Runnable updater = new Runnable() {
            @Override
            public void run() {
                invalidateSelf();
            }
        };
        private long startedAt;
        private boolean running;

        MovieDrawable(Movie movie) {
            this.movie = movie;
        }

        @Override
        public void draw(Canvas canvas) {
            if (running) {
                long now = SystemClock.uptimeMillis();
                if (startedAt == 0L) {
                    startedAt = now;
                }
                int duration = movie.duration() <= 0 ? 1000 : movie.duration();
                movie.setTime((int) ((now - startedAt) % duration));
            } else {
                movie.setTime(0);
            }

            Rect bounds = getBounds();
            int width = Math.max(1, movie.width());
            int height = Math.max(1, movie.height());
            float scale = Math.min(bounds.width() / (float) width, bounds.height() / (float) height);
            float dx = bounds.left + (bounds.width() - width * scale) / 2f;
            float dy = bounds.top + (bounds.height() - height * scale) / 2f;

            canvas.save();
            canvas.translate(dx, dy);
            canvas.scale(scale, scale);
            movie.draw(canvas, 0, 0, paint);
            canvas.restore();

            if (running) {
                scheduleSelf(updater, SystemClock.uptimeMillis() + 33);
            }
        }

        @Override
        public void setAlpha(int alpha) {
            paint.setAlpha(alpha);
        }

        @Override
        public void setColorFilter(android.graphics.ColorFilter colorFilter) {
            paint.setColorFilter(colorFilter);
        }

        @Override
        public int getOpacity() {
            return android.graphics.PixelFormat.TRANSLUCENT;
        }

        @Override
        public int getIntrinsicWidth() {
            return movie.width();
        }

        @Override
        public int getIntrinsicHeight() {
            return movie.height();
        }

        @Override
        public void start() {
            if (running) {
                return;
            }
            running = true;
            startedAt = SystemClock.uptimeMillis();
            invalidateSelf();
        }

        @Override
        public void stop() {
            running = false;
            unscheduleSelf(updater);
        }

        @Override
        public boolean isRunning() {
            return running;
        }
    }

    private void openExternal(String url) {
        if (!isWebUrl(url)) {
            Toast.makeText(this, "这不是可在浏览器打开的网页链接", Toast.LENGTH_SHORT).show();
            return;
        }
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            intent.addCategory(Intent.CATEGORY_BROWSABLE);
            startActivity(intent);
        } catch (Exception ignored) {
            Toast.makeText(this, "无法打开该链接", Toast.LENGTH_SHORT).show();
        }
    }

    private TextView externalLinkText(String label, final String url, int sizeSp) {
        TextView link = text(label, sizeSp, Typeface.NORMAL, BLUE);
        link.setPaintFlags(link.getPaintFlags() | Paint.UNDERLINE_TEXT_FLAG);
        link.setContentDescription("在浏览器打开：" + url);
        link.setOnClickListener(v -> openExternal(url));
        link.setPadding(0, dp(4), 0, dp(4));
        return link;
    }

    private boolean isWebUrl(String value) {
        return value != null && (value.startsWith("http://") || value.startsWith("https://"));
    }

    private boolean isImageUrl(String value) {
        if (value == null) {
            return false;
        }
        String lower = value.toLowerCase(Locale.ROOT);
        return lower.endsWith(".gif") || lower.endsWith(".png") || lower.endsWith(".jpg")
                || lower.endsWith(".jpeg") || lower.endsWith(".webp");
    }

    private TextView section(String value) {
        return text(value, 16, Typeface.BOLD, INK);
    }

    private void addNumberedSteps(LinearLayout container, List<String> steps) {
        for (int i = 0; i < steps.size(); i++) {
            LinearLayout row = new LinearLayout(this);
            row.setOrientation(LinearLayout.HORIZONTAL);
            TextView num = text(String.valueOf(i + 1), 13, Typeface.BOLD, Color.WHITE);
            num.setGravity(Gravity.CENTER);
            num.setBackground(bg(GREEN, dp(11), GREEN, 0));
            LinearLayout.LayoutParams numLp = new LinearLayout.LayoutParams(dp(22), dp(22));
            numLp.setMargins(0, dp(2), dp(10), 0);
            row.addView(num, numLp);
            TextView body = text(steps.get(i), 15, Typeface.NORMAL, INK);
            row.addView(body, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
            LinearLayout.LayoutParams rowLp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            rowLp.setMargins(0, dp(5), 0, dp(5));
            container.addView(row, rowLp);
        }
    }

    private TextView smallLabel(String value) {
        TextView label = text(value, 12, Typeface.BOLD, GREEN);
        label.setAllCaps(false);
        return label;
    }

    private TextView text(String value, int sp, int style, int color) {
        TextView text = new TextView(this);
        text.setText(value == null ? "" : value);
        text.setTextSize(sp);
        text.setTextColor(color);
        text.setTypeface(Typeface.DEFAULT, style);
        text.setLineSpacing(0, 1.08f);
        return text;
    }

    private View noteBox(String value, int accent) {
        TextView note = text(value, 14, Typeface.NORMAL, INK);
        note.setPadding(dp(12), dp(10), dp(12), dp(10));
        note.setBackground(bg(Color.rgb(249, 251, 247), dp(8), accent, 2));
        return note;
    }

    private Button chip(String label, boolean selected, View.OnClickListener listener) {
        Button chip = button(label, selected ? GREEN : Color.rgb(236, 240, 234),
                selected ? Color.WHITE : INK, listener);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, dp(38));
        params.setMargins(0, 0, dp(8), dp(8));
        chip.setLayoutParams(params);
        chip.setMinWidth(dp(58));
        return chip;
    }

    private Button button(String label, int bgColor, int textColor, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setTextSize(14);
        button.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        button.setAllCaps(false);
        button.setGravity(Gravity.CENTER);
        button.setPadding(dp(10), 0, dp(10), 0);
        button.setMinHeight(dp(38));
        restyleButton(button, bgColor, textColor);
        button.setOnClickListener(listener);
        return button;
    }

    private void restyleButton(Button button, int bgColor, int textColor) {
        boolean lightBg = isLight(bgColor);
        GradientDrawable shape = bg(bgColor, dp(10), lightBg ? LINE : bgColor, lightBg ? 1 : 0);
        int ripple = lightBg ? Color.argb(28, 0, 0, 0) : Color.argb(60, 255, 255, 255);
        button.setBackground(new RippleDrawable(ColorStateList.valueOf(ripple), shape, null));
        button.setTextColor(textColor);
    }

    private void styleChip(Button chip, boolean selected) {
        restyleButton(chip, selected ? GREEN : Color.rgb(236, 240, 234), selected ? Color.WHITE : INK);
    }

    private boolean isLight(int color) {
        double luminance = (0.299 * Color.red(color) + 0.587 * Color.green(color) + 0.114 * Color.blue(color)) / 255.0;
        return luminance > 0.7;
    }

    private GradientDrawable bg(int color, int radius, int strokeColor, int strokeWidth) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(radius);
        if (strokeWidth > 0) {
            drawable.setStroke(strokeWidth, strokeColor);
        }
        return drawable;
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private View space(int dp) {
        Space space = new Space(this);
        space.setLayoutParams(new LinearLayout.LayoutParams(dp(dp), dp(dp)));
        return space;
    }

    private String join(List<String> values) {
        if (values == null || values.isEmpty()) {
            return "无";
        }
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < values.size(); i++) {
            if (i > 0) {
                builder.append(" / ");
            }
            builder.append(values.get(i));
        }
        return builder.toString();
    }

    private String painSummary() {
        List<String> values = new ArrayList<String>();
        if (shoulderPain != null) {
            values.add("肩" + shoulderPain.label());
        }
        if (lowerBackPain != null) {
            values.add("腰" + lowerBackPain.label());
        }
        if (kneePain != null) {
            values.add("膝" + kneePain.label());
        }
        return values.isEmpty() ? "无" : join(values);
    }

    private int dp(int value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }

    private interface SeveritySetter {
        void set(PainSeverity severity);
    }

    private interface ChipPick {
        void pick(String value);
    }

    private static final class RecipeStep {
        private String text = "";
        private String image = "";

        private RecipeStep() {
        }

        private RecipeStep(String text, String image) {
            this.text = text == null ? "" : text;
            this.image = image == null ? "" : image;
        }
    }

    private static final class PreparedImage {
        private final byte[] bytes;
        private final String mimeType;

        private PreparedImage(byte[] bytes, String mimeType) {
            this.bytes = bytes;
            this.mimeType = mimeType;
        }
    }

    private static final class Recipe {
        private String id = "";
        private String name = "";
        private String sourceMedia = "";
        private String sourceUrl = "";
        private String note = "";
        private String review = "";
        private int rating;
        private long createdAt;
        private final List<String> tags = new ArrayList<String>();
        private final List<String> photos = new ArrayList<String>();
        private final List<String> ingredients = new ArrayList<String>();
        private final List<RecipeStep> steps = new ArrayList<RecipeStep>();
        /** 收进来的循证食谱 id：非空表示这道菜有科学依据可查，也用来去重。 */
        private String builtinId = "";
        /** 营养估算：知道了才能按热量推荐、才能一键记入今日。0 表示未知。 */
        private int kcal;
        private int proteinG;
        private int fiberG;
        private final Map<FoodGroup, Integer> groupGrams =
                new EnumMap<FoodGroup, Integer>(FoodGroup.class);

        private boolean hasNutrition() {
            return kcal > 0 || !groupGrams.isEmpty();
        }
    }

    private static final class PendingShare {
        private final String title;
        private final String body;
        private final String uri;
        private final String createdAt;

        private PendingShare(String title, String body, String uri, String createdAt) {
            this.title = title;
            this.body = body;
            this.uri = uri;
            this.createdAt = createdAt;
        }
    }

    private static final class SessionRecord {
        private final String time;
        private final String title;
        private final int total;
        private final int done;
        private final String feel;
        private final String pain;
        private final String note;
        private final List<String> itemLines;
        /** 结构化的动作结果 "动作id|组数|是否完成"，周容量台账和恢复状态靠它。 */
        private final List<String> itemStats;
        private final String duration;
        private final long epochMillis;        // 训练结束时刻
        private final long startEpochMillis;   // 训练开始时刻；心率统计窗口用它，不再靠时长字符串反推
        private final int hrAvg;
        private final int hrMax;
        private final int hrMin;
        private final String hrSeries;
        private final int hrSamples;
        private final int hrCoveragePercent;
        private final boolean hrReliable;       // 采样够密才算这次训练真正的心率
        private final String hrSource;          // 数据来自哪个 App / 手表运动记录
        private List<WorkoutEntry> details = new ArrayList<>();
        private JSONObject metrics = new JSONObject();
        private String timingNote = "";

        private SessionRecord copyExtras(SessionRecord from) {
            details = new ArrayList<>(from.details); metrics = from.metrics; timingNote = from.timingNote; return this;
        }

        private SessionRecord(String time, String title, int total, int done,
                String feel, String pain, String note, List<String> itemLines, String duration,
                long epochMillis) {
            this(time, title, total, done, feel, pain, note, itemLines, duration, epochMillis,
                    0L, 0, 0, 0, "", 0, 0, false, "", null);
        }

        private SessionRecord(String time, String title, int total, int done,
                String feel, String pain, String note, List<String> itemLines, String duration,
                long epochMillis, long startEpochMillis, int hrAvg, int hrMax, int hrMin,
                String hrSeries, int hrSamples, int hrCoveragePercent, boolean hrReliable,
                String hrSource) {
            this(time, title, total, done, feel, pain, note, itemLines, duration, epochMillis,
                    startEpochMillis, hrAvg, hrMax, hrMin, hrSeries, hrSamples, hrCoveragePercent,
                    hrReliable, hrSource, null);
        }

        private SessionRecord(String time, String title, int total, int done,
                String feel, String pain, String note, List<String> itemLines, String duration,
                long epochMillis, long startEpochMillis, int hrAvg, int hrMax, int hrMin,
                String hrSeries, int hrSamples, int hrCoveragePercent, boolean hrReliable,
                String hrSource, List<String> itemStats) {
            this.itemStats = itemStats == null ? new ArrayList<String>() : itemStats;
            this.time = time == null ? "" : time;
            this.title = title == null ? "" : title;
            this.total = total;
            this.done = done;
            this.feel = feel == null ? "" : feel;
            this.pain = pain == null ? "" : pain;
            this.note = note == null ? "" : note;
            this.itemLines = itemLines == null ? new ArrayList<String>() : itemLines;
            this.duration = duration == null ? "" : duration;
            this.epochMillis = epochMillis;
            this.startEpochMillis = startEpochMillis;
            this.hrAvg = hrAvg;
            this.hrMax = hrMax;
            this.hrMin = hrMin;
            this.hrSeries = hrSeries == null ? "" : hrSeries;
            this.hrSamples = hrSamples;
            this.hrCoveragePercent = hrCoveragePercent;
            this.hrReliable = hrReliable;
            this.hrSource = hrSource == null ? "" : hrSource;
        }

        private SessionRecord withHeartRate(HeartRateStats stats, String series, String source) {
            return new SessionRecord(time, title, total, done, feel, pain, note, itemLines,
                    duration, epochMillis, startEpochMillis, stats.average(), stats.max(),
                    stats.min(), series, stats.sampleCount(),
                    (int) Math.round(stats.coverage() * 100), stats.isReliable(), source,
                    itemStats).copyExtras(this);
        }

        /** 训练窗口：没有记录开始时刻的老数据回落到「结束时刻 − 时长」。 */
        private long windowStartMillis(long durationSeconds) {
            if (startEpochMillis > 0) {
                return startEpochMillis;
            }
            return epochMillis - Math.max(0, durationSeconds) * 1000L;
        }

        private static SessionRecord legacy(String text) {
            return new SessionRecord(text, "", 0, 0, "", "", "", new ArrayList<String>(), "", 0L);
        }

        private String summary() {
            if (title.length() == 0) {
                return time;
            }
            return time + " · " + title + " · 完成 " + done + "/" + total + " 个动作";
        }
    }
}
