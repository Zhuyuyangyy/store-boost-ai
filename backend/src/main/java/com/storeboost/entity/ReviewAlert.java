package com.storeboost.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("review_alert")
public class ReviewAlert {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long shopId;
    private String platform;
    private String reviewerName;
    private Integer rating;
    private Double negativeScore;
    private String content;
    private String aiSuggestion;
    private String aiReply;
    private Integer replyStatus;
    private String replyAdopted;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}