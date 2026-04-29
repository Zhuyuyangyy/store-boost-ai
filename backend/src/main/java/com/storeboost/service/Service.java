package com.storeboost.service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.storeboost.entity.*;
import com.storeboost.mapper.*;
import com.storeboost.dto.*;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

@Service
public class ShopService extends ServiceImpl<ShopMapper, Shop> {
    public Shop register(ShopRegisterDTO dto) {
        Shop shop = new Shop();
        shop.setName(dto.getName());
        shop.setCategory(dto.getCategory());
        shop.setAddress(dto.getAddress());
        shop.setContact(dto.getContact());
        shop.setDescription(dto.getDescription());
        this.save(shop);
        return shop;
    }

    public List<Shop> listAll() {
        return this.list();
    }

    public Shop getById(Long id) {
        return this.getById(id);
    }
}

@Service
public class FootTrafficService extends ServiceImpl<FootTrafficMapper, FootTraffic> {
    public boolean saveData(FootTrafficDTO dto) {
        FootTraffic ft = new FootTraffic();
        ft.setShopId(dto.getShopId());
        ft.setDate(LocalDate.parse(dto.getDate()));
        ft.setTotalPassers(dto.getTotalPassers());
        ft.setTotalEnter(dto.getTotalEnter());
        ft.setEnterRate(dto.getEnterRate());
        ft.setAvgStaySeconds(dto.getAvgStaySeconds());
        ft.setMaleRatio(dto.getMaleRatio());
        ft.setFemaleRatio(dto.getFemaleRatio());
        ft.setPeakHour(dto.getPeakHour());
        return this.save(ft);
    }

    public List<Map<String, Object>> getWeeklyTrend(Long shopId) {
        LocalDate end = LocalDate.now();
        LocalDate start = end.minusDays(6);
        QueryWrapper<FootTraffic> q = new QueryWrapper<>();
        q.eq("shop_id", shopId).between("date", start, end).orderByAsc("date");
        List<FootTraffic> list = this.list(q);
        List<Map<String, Object>> result = new ArrayList<>();
        for (FootTraffic ft : list) {
            Map<String, Object> m = new HashMap<>();
            m.put("date", ft.getDate());
            m.put("passers", ft.getTotalPassers());
            m.put("enter", ft.getTotalEnter());
            m.put("enterRate", ft.getEnterRate());
            result.add(m);
        }
        return result;
    }
}

@Service
public class ContentCalendarService extends ServiceImpl<ContentCalendarMapper, ContentCalendar> {
    public ContentCalendar create(ContentCalendarDTO dto) {
        ContentCalendar c = new ContentCalendar();
        c.setShopId(dto.getShopId());
        c.setPlanDate(LocalDate.parse(dto.getPlanDate()));
        c.setContentType(dto.getContentType());
        c.setPublishStatus(0);
        this.save(c);
        return c;
    }

    public List<ContentCalendar> getByShop(Long shopId) {
        QueryWrapper<ContentCalendar> q = new QueryWrapper<>();
        q.eq("shop_id", shopId).orderByAsc("plan_date");
        return this.list(q);
    }

    public boolean updateScript(Long id, String aiScript, String hookText, String bodyText, String ctaText, String hashtags, String bestTime) {
        ContentCalendar c = this.getById(id);
        if (c == null) return false;
        c.setAiScript(aiScript);
        c.setHookText(hookText);
        c.setBodyText(bodyText);
        c.setCtaText(ctaText);
        c.setHashtags(hashtags);
        c.setBestTime(bestTime);
        return this.updateById(c);
    }
}

@Service
public class ReviewAlertService extends ServiceImpl<ReviewAlertMapper, ReviewAlert> {
    public boolean saveAlert(ReviewAlertDTO dto) {
        ReviewAlert r = new ReviewAlert();
        r.setShopId(dto.getShopId());
        r.setPlatform(dto.getPlatform());
        r.setReviewerName(dto.getReviewerName());
        r.setRating(dto.getRating());
        r.setContent(dto.getContent());
        // 简单负面评分：评分<=2为高风险
        double score = dto.getRating() <= 2 ? 0.8 : dto.getRating() == 3 ? 0.4 : 0.1;
        r.setNegativeScore(score);
        r.setReplyStatus(0);
        return this.save(r);
    }

    public List<ReviewAlert> getAlerts(Long shopId) {
        QueryWrapper<ReviewAlert> q = new QueryWrapper<>();
        q.eq("shop_id", shopId).orderByDesc("created_at");
        return this.list(q);
    }

    public boolean saveReply(Long id, String aiReply) {
        ReviewAlert r = this.getById(id);
        if (r == null) return false;
        r.setAiReply(aiReply);
        r.setReplyStatus(1);
        return this.updateById(r);
    }
}