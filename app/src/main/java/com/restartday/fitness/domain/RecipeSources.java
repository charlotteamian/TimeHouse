package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * 联网找菜时允许参考的站点白名单。
 *
 * <p>存在的理由：不限来源地搜「今天吃什么」，AI 很容易搜到内容农场和聚合站——
 * 用量含糊、步骤缺火候时间，甚至根本没人做过。这里锁死在有真实用量和步骤的菜谱站，
 * 提示词里给出名单，返回的链接再按域名校验一次，两道都过才认。
 *
 * <p>营养站（{@link Site#recipeSource()} 为 false）只用来校对热量和依据，
 * 不能当菜谱来源——它们没有做法。
 */
public final class RecipeSources {

    /** 一个允许的站点：主域名 + 中文名 + 能不能当菜谱来源。 */
    public static final class Site {
        private final String host;
        private final String label;
        private final boolean recipeSource;

        private Site(String host, String label, boolean recipeSource) {
            this.host = host;
            this.label = label;
            this.recipeSource = recipeSource;
        }

        public String host() {
            return host;
        }

        public String label() {
            return label;
        }

        /** true = 可作为菜谱来源；false = 只用于校对营养数据。 */
        public boolean recipeSource() {
            return recipeSource;
        }
    }

    private static final List<Site> SITES;

    static {
        List<Site> sites = new ArrayList<Site>();
        sites.add(new Site("xiachufang.com", "下厨房", true));
        sites.add(new Site("meishij.net", "美食杰", true));
        sites.add(new Site("douguo.com", "豆果美食", true));
        sites.add(new Site("meishichina.com", "美食天下", true));
        sites.add(new Site("xinshipu.com", "心食谱", true));
        sites.add(new Site("boohee.com", "薄荷健康", false));
        sites.add(new Site("cnsoc.org", "中国营养学会", false));
        SITES = Collections.unmodifiableList(sites);
    }

    private RecipeSources() {
    }

    public static List<Site> sites() {
        return SITES;
    }

    /**
     * 取出 http(s) 链接的主机名，小写。取不出来（不是 http(s)、没有主机）返回空串。
     *
     * <p>先砍 path/query/fragment，再砍 userinfo，最后砍端口：
     * {@code https://xiachufang.com@evil.com/x} 的真实主机是 evil.com，不能被前半段骗过去。
     */
    public static String host(String url) {
        if (url == null) {
            return "";
        }
        String value = url.trim();
        String lower = value.toLowerCase();
        if (lower.startsWith("https://")) {
            value = value.substring(8);
        } else if (lower.startsWith("http://")) {
            value = value.substring(7);
        } else {
            return "";
        }
        int cut = value.length();
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (c == '/' || c == '?' || c == '#') {
                cut = i;
                break;
            }
        }
        String authority = value.substring(0, cut);
        int at = authority.lastIndexOf('@');
        if (at >= 0) {
            authority = authority.substring(at + 1);
        }
        int colon = authority.indexOf(':');
        if (colon >= 0) {
            authority = authority.substring(0, colon);
        }
        return authority.toLowerCase();
    }

    /** 白名单内（含子域名）返回对应站点，否则 null。 */
    public static Site match(String url) {
        String host = host(url);
        if (host.length() == 0) {
            return null;
        }
        for (Site site : SITES) {
            if (host.equals(site.host()) || host.endsWith("." + site.host())) {
                return site;
            }
        }
        return null;
    }

    public static boolean isAllowed(String url) {
        return match(url) != null;
    }

    /** 能不能当菜谱来源：既要在白名单里，还得是菜谱站而不是营养数据站。 */
    public static boolean isRecipeSource(String url) {
        Site site = match(url);
        return site != null && site.recipeSource();
    }

    /** 站点中文名，用于「来源：下厨房」这样的显示；不在白名单返回空串。 */
    public static String labelFor(String url) {
        Site site = match(url);
        return site == null ? "" : site.label();
    }

    /** 写进提示词的菜谱站名单。 */
    public static String recipePromptList() {
        return promptList(true);
    }

    /** 写进提示词的营养校对站名单。 */
    public static String nutritionPromptList() {
        return promptList(false);
    }

    private static String promptList(boolean recipeSource) {
        StringBuilder builder = new StringBuilder();
        for (Site site : SITES) {
            if (site.recipeSource() != recipeSource) {
                continue;
            }
            if (builder.length() > 0) {
                builder.append("、");
            }
            builder.append(site.label()).append("（").append(site.host()).append("）");
        }
        return builder.toString();
    }
}
