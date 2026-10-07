package com.restartday.fitness.domain;

public final class RecipeSourcesTest {
    public static void main(String[] args) {
        RecipeSourcesTest test = new RecipeSourcesTest();
        test.acceptsWhitelistedSitesAndSubdomains();
        test.rejectsLookalikeHosts();
        test.rejectsNonHttpAndJunk();
        test.nutritionSitesAreNotRecipeSources();
        test.promptListsSplitRecipeAndNutritionSites();
        System.out.println("RecipeSourcesTest: all tests passed");
    }

    private void acceptsWhitelistedSitesAndSubdomains() {
        assertTrue(RecipeSources.isRecipeSource("https://www.xiachufang.com/recipe/100234/"),
                "下厨房正常链接应通过");
        assertTrue(RecipeSources.isRecipeSource("https://m.xiachufang.com/recipe/100234/"),
                "子域名应通过");
        assertTrue(RecipeSources.isRecipeSource("http://www.meishij.net/zuofa/abc.html"),
                "http 也应通过");
        assertTrue(RecipeSources.isRecipeSource("https://www.douguo.com/cookbook/123.html?from=app"),
                "带 query 应通过");
        assertTrue(RecipeSources.labelFor("https://www.xiachufang.com/recipe/1/").equals("下厨房"),
                "应能取出站点中文名");
        assertTrue(RecipeSources.host("https://WWW.XiaChuFang.com:443/recipe/1/")
                        .equals("www.xiachufang.com"),
                "主机名应小写并去掉端口，实际 "
                        + RecipeSources.host("https://WWW.XiaChuFang.com:443/recipe/1/"));
    }

    private void rejectsLookalikeHosts() {
        // AI 返回的链接不能只看「字符串里有没有 xiachufang」，否则这三种全都能骗过去。
        assertTrue(!RecipeSources.isAllowed("https://xiachufang.com.evil.com/recipe/1"),
                "前缀相同的钓鱼域名应拒绝");
        assertTrue(!RecipeSources.isAllowed("https://evil.com/www.xiachufang.com/recipe/1"),
                "把白名单塞进 path 应拒绝");
        assertTrue(!RecipeSources.isAllowed("https://xiachufang.com@evil.com/recipe/1"),
                "userinfo 伪装应按真实主机 evil.com 拒绝");
        assertTrue(!RecipeSources.isAllowed("https://notxiachufang.com/recipe/1"),
                "仅后缀相同应拒绝");
    }

    private void rejectsNonHttpAndJunk() {
        assertTrue(!RecipeSources.isAllowed("javascript:alert(1)"), "非 http(s) 应拒绝");
        assertTrue(!RecipeSources.isAllowed("xiachufang.com/recipe/1"), "没有协议头应拒绝");
        assertTrue(!RecipeSources.isAllowed(""), "空串应拒绝");
        assertTrue(!RecipeSources.isAllowed(null), "null 应拒绝");
        assertTrue(RecipeSources.host("ftp://xiachufang.com").length() == 0, "非 http(s) 取不出主机");
    }

    private void nutritionSitesAreNotRecipeSources() {
        // 薄荷和营养学会没有做法，只能用来校对热量，不能当「今天吃这个」的来源。
        assertTrue(RecipeSources.isAllowed("https://www.boohee.com/food/group/1"),
                "营养站应在白名单内");
        assertTrue(!RecipeSources.isRecipeSource("https://www.boohee.com/food/group/1"),
                "营养站不应当作菜谱来源");
        assertTrue(!RecipeSources.isRecipeSource("https://www.cnsoc.org/scienceNews/1.html"),
                "中国营养学会不应当作菜谱来源");
    }

    private void promptListsSplitRecipeAndNutritionSites() {
        String recipeList = RecipeSources.recipePromptList();
        assertTrue(recipeList.contains("下厨房") && recipeList.contains("xiachufang.com"),
                "菜谱名单应含下厨房，实际 " + recipeList);
        assertTrue(!recipeList.contains("薄荷健康"), "菜谱名单不应混入营养站");
        assertTrue(RecipeSources.nutritionPromptList().contains("薄荷健康"),
                "营养名单应含薄荷健康");
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
