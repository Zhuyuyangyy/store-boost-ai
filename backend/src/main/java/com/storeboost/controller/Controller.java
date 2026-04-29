package com.storeboost.controller;

import com.storeboost.dto.ShopRegisterDTO;
import com.storeboost.entity.Shop;
import com.storeboost.service.ShopService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/shop")
@CrossOrigin
public class ShopController {

    @Autowired
    private ShopService shopService;

    @PostMapping("/register")
    public Map<String, Object> register(@RequestBody ShopRegisterDTO dto) {
        Shop shop = shopService.register(dto);
        return Map.of("success", true, "shopId", shop.getId(), "message", "店铺注册成功");
    }

    @GetMapping("/list")
    public Map<String, Object> list() {
        List<Shop> shops = shopService.list();
        return Map.of("success", true, "data", shops);
    }

    @GetMapping("/{id}")
    public Map<String, Object> getById(@PathVariable Long id) {
        Shop shop = shopService.getById(id);
        return Map.of("success", true, "data", shop);
    }
}

package com.storeboost.controller;

import com.storeboost.dto.FootTrafficDTO;
import com.storeboost.service.FootTrafficService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/foot-traffic")
@CrossOrigin
public class FootTrafficController {

    @Autowired
    private FootTrafficService footTrafficService;

    @PostMapping
    public Map<String, Object> save(@RequestBody FootTrafficDTO dto) {
        boolean ok = footTrafficService.saveData(dto);
        return Map.of("success", ok, "message", ok ? "保存成功" : "保存失败");
    }

    @GetMapping("/{shopId}/weekly")
    public Map<String, Object> weekly(@PathVariable Long shopId) {
        List<Map<String, Object>> data = footTrafficService.getWeeklyTrend(shopId);
        return Map.of("success", true, "data", data);
    }
}

package com.storeboost.controller;

import com.storeboost.dto.ContentCalendarDTO;
import com.storeboost.service.ContentCalendarService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/content")
@CrossOrigin
public class ContentController {

    @Autowired
    private ContentCalendarService contentService;

    @PostMapping("/calendar")
    public Map<String, Object> create(@RequestBody ContentCalendarDTO dto) {
        var c = contentService.create(dto);
        return Map.of("success", true, "id", c.getId(), "message", "日程创建成功");
    }

    @GetMapping("/calendar/{shopId}")
    public Map<String, Object> list(@PathVariable Long shopId) {
        List<?> list = contentService.getByShop(shopId);
        return Map.of("success", true, "data", list);
    }

    @PostMapping("/script/generate")
    public Map<String, Object> generateScript(@RequestBody Map<String, Object> req) {
        Long id = ((Number) req.get("calendarId")).longValue();
        // AI脚本生成暂时返回固定内容（后续接AI服务）
        String script = "【开场钩子】老板们注意了！这家店" + req.getOrDefault("shopName", "门店") + "的秘密，今天告诉你！\n\n" +
                "【正文】今天来聊聊我们店里的" + req.getOrDefault("category", "招牌产品") + "，为什么这么多人来排队？" +
                "因为我们坚持用最新鲜的食材，价格实惠，服务热情。\n\n" +
                "【行动号召】喜欢的话点个赞关注一下，下次给你更多优惠！\n\n" +
                "#本地美食 #" + req.getOrDefault("category", "美食") + " #探店";
        String hook = "老板们注意了！" + req.getOrDefault("shopName", "门店") + "的秘密今天公开";
        String body = script;
        String cta = "喜欢的话点个赞关注一下，下次给你更多优惠！";
        String hashtags = "#本地美食 #" + req.getOrDefault("category", "美食") + " #探店 #" + req.getOrDefault("city", "本地");
        String bestTime = "12:00,19:00";

        contentService.updateScript(id, script, hook, body, cta, hashtags, bestTime);
        return Map.of("success", true, "hook", hook, "body", body, "cta", cta, "hashtags", hashtags, "bestTime", bestTime);
    }
}

package com.storeboost.controller;

import com.storeboost.dto.ReviewAlertDTO;
import com.storeboost.service.ReviewAlertService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/review")
@CrossOrigin
public class ReviewController {

    @Autowired
    private ReviewAlertService reviewService;

    @PostMapping("/sync")
    public Map<String, Object> sync(@RequestBody ReviewAlertDTO dto) {
        boolean ok = reviewService.saveAlert(dto);
        return Map.of("success", ok, "message", ok ? "差评录入成功" : "录入失败");
    }

    @GetMapping("/alerts/{shopId}")
    public Map<String, Object> alerts(@PathVariable Long shopId) {
        List<?> alerts = reviewService.getAlerts(shopId);
        return Map.of("success", true, "data", alerts);
    }

    @PostMapping("/reply")
    public Map<String, Object> reply(@RequestBody Map<String, Object> req) {
        Long id = ((Number) req.get("alertId")).longValue();
        String reply = (String) req.get("reply");
        boolean ok = reviewService.saveReply(id, reply);
        return Map.of("success", ok, "message", ok ? "回复已保存" : "保存失败");
    }
}

package com.storeboost.controller;

import com.storeboost.entity.*;
import com.storeboost.service.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/dashboard")
@CrossOrigin
public class DashboardController {

    @Autowired private ShopService shopService;
    @Autowired private FootTrafficService footTrafficService;
    @Autowired private ContentCalendarService contentService;
    @Autowired private ReviewAlertService reviewService;

    @GetMapping("/{shopId}")
    public Map<String, Object> dashboard(@PathVariable Long shopId) {
        // 客流趋势
        List<Map<String, Object>> traffic = footTrafficService.getWeeklyTrend(shopId);
        // 内容日历
        List<?> calendars = contentService.getByShop(shopId);
        // 差评统计
        List<?> alerts = reviewService.getAlerts(shopId);
        long pendingAlerts = alerts.stream().filter(a -> {
            if (a instanceof ReviewAlert) return ((ReviewAlert) a).getReplyStatus() == 0;
            return true;
        }).count();
        // 店铺信息
        Shop shop = shopService.getById(shopId);

        return Map.of(
            "success", true,
            "shop", shop,
            "traffic", traffic,
            "calendars", calendars,
            "alertCount", alerts.size(),
            "pendingAlerts", pendingAlerts,
            "message", "数据加载成功"
        );
    }
}