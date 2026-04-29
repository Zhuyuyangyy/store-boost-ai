package com.storeboost.dto;

import lombok.Data;

@Data
public class ShopRegisterDTO {
    private String name;
    private String category;
    private String address;
    private String contact;
    private String description;
}

package com.storeboost.dto;

import lombok.Data;

@Data
public class FootTrafficDTO {
    private Long shopId;
    private String date;
    private Integer totalPassers;
    private Integer totalEnter;
    private Double enterRate;
    private Integer avgStaySeconds;
    private Double maleRatio;
    private Double femaleRatio;
    private String peakHour;
}

package com.storeboost.dto;

import lombok.Data;

@Data
public class ContentCalendarDTO {
    private Long shopId;
    private String planDate;
    private String contentType;
}

package com.storeboost.dto;

import lombok.Data;

@Data
public class ReviewAlertDTO {
    private Long shopId;
    private String platform;
    private String reviewerName;
    private Integer rating;
    private String content;
}

package com.storeboost.dto;

import lombok.Data;

@Data
public class ReviewReplyDTO {
    private Long alertId;
    private String chosenReply;
}