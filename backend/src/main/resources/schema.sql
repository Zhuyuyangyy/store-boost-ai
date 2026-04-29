-- StoreBoost AI 数据库初始化脚本
CREATE DATABASE IF NOT EXISTS store_boost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE store_boost;

-- 1. 店铺表
CREATE TABLE shop (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '店名',
    category VARCHAR(50) COMMENT '品类：餐饮/美业/零售/健身房/宠物/其他',
    address VARCHAR(255) COMMENT '地址',
    contact VARCHAR(50) COMMENT '联系方式',
    description VARCHAR(500) COMMENT '店铺简介',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 客流数据表
CREATE TABLE foot_traffic (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL COMMENT '店铺ID',
    date DATE NOT NULL COMMENT '统计日期',
    total_passers INT DEFAULT 0 COMMENT '经过人数',
    total_enter INT DEFAULT 0 COMMENT '进店人数',
    enter_rate DECIMAL(5,2) DEFAULT 0.00 COMMENT '进店率%',
    avg_stay_seconds INT DEFAULT 0 COMMENT '平均停留时长(秒)',
    male_ratio DECIMAL(5,2) DEFAULT 0.00 COMMENT '男性占比%',
    female_ratio DECIMAL(5,2) DEFAULT 0.00 COMMENT '女性占比%',
    peak_hour VARCHAR(100) COMMENT '高峰时段，多个用逗号分隔',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id),
    UNIQUE KEY uk_shop_date (shop_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 内容日历表
CREATE TABLE content_calendar (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    plan_date DATE NOT NULL COMMENT '计划发布日',
    content_type VARCHAR(30) COMMENT '类型：种草/促销/展示/热点',
    video_theme VARCHAR(200) COMMENT '视频主题',
    ai_script TEXT COMMENT 'AI生成的脚本',
    hook_text VARCHAR(200) COMMENT '开头钩子',
    body_text TEXT COMMENT '正文内容',
    cta_text VARCHAR(100) COMMENT '行动号召',
    hashtags VARCHAR(200) COMMENT '推荐标签',
    best_time VARCHAR(20) COMMENT '最佳发布时间',
    publish_status TINYINT DEFAULT 0 COMMENT '0未发 1已发 2跳过',
    published_at DATETIME COMMENT '实际发布时间',
    views INT DEFAULT 0 COMMENT '播放量',
    likes INT DEFAULT 0 COMMENT '点赞数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id),
    UNIQUE KEY uk_shop_plan_date (shop_id, plan_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 差评预警表
CREATE TABLE review_alert (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    platform VARCHAR(30) COMMENT 'dianping/meituan/xiaohongshu/其他',
    reviewer_name VARCHAR(100) COMMENT '评价者',
    rating INT COMMENT '评分 1-5',
    negative_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '负面情绪得分 0-1',
    content TEXT COMMENT '评价内容',
    ai_suggestion TEXT COMMENT 'AI整改建议',
    ai_reply TEXT COMMENT 'AI生成回复话术',
    reply_status TINYINT DEFAULT 0 COMMENT '0未回复 1已回复 2已采纳',
    reply_adopted VARCHAR(200) COMMENT '已采纳的回复',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 数据看板汇总表
CREATE TABLE dashboard_stats (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    stat_date DATE NOT NULL COMMENT '统计日期',
    content_views INT DEFAULT 0 COMMENT '内容总播放',
    content_likes INT DEFAULT 0 COMMENT '总点赞',
    content_comments INT DEFAULT 0 COMMENT '总评论',
    content_shares INT DEFAULT 0 COMMENT '总分享',
    new_followers INT DEFAULT 0 COMMENT '新增关注',
    guide_orders INT DEFAULT 0 COMMENT '引导订单',
    guide_revenue DECIMAL(10,2) DEFAULT 0.00 COMMENT '引导营收',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id),
    UNIQUE KEY uk_shop_stat_date (shop_id, stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 初始插入一条测试数据
INSERT INTO shop (name, category, address, contact) VALUES
('老王家常菜', '餐饮', '北京市朝阳区望京街道', '13800138000'),
('美颜阁美容店', '美业', '上海市静安区南京西路', '13900139000');