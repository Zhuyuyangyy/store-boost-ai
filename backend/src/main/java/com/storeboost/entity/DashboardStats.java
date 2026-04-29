package com.storeboost.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("dashboard_stats")
public class DashboardStats {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long shopId;
    private LocalDate statDate;
    private Integer contentViews;
    private Integer contentLikes;
    private Integer contentComments;
    private Integer contentShares;
    private Integer newFollowers;
    private Integer guideOrders;
    private Double guideRevenue;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}