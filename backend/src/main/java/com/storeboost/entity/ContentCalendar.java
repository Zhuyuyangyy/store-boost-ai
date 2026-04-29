package com.storeboost.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("content_calendar")
public class ContentCalendar {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long shopId;
    private LocalDate planDate;
    private String contentType;
    private String videoTheme;
    private String aiScript;
    private String hookText;
    private String bodyText;
    private String ctaText;
    private String hashtags;
    private String bestTime;
    private Integer publishStatus;
    private LocalDateTime publishedAt;
    private Integer views;
    private Integer likes;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}