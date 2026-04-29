package com.storeboost.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("foot_traffic")
public class FootTraffic {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long shopId;
    private LocalDate date;
    private Integer totalPassers;
    private Integer totalEnter;
    private Double enterRate;
    private Integer avgStaySeconds;
    private Double maleRatio;
    private Double femaleRatio;
    private String peakHour;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}