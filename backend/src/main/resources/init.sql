-- StoreBoost AI MySQL初始化（MySQL 8.0）
-- 运行命令: mysql -u root -p < init.sql

CREATE DATABASE IF NOT EXISTS store_boost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE store_boost;

CREATE TABLE IF NOT EXISTS shop (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '店名',
    category VARCHAR(50) COMMENT '品类',
    address VARCHAR(255) COMMENT '地址',
    contact VARCHAR(50) COMMENT '联系方式',
    description VARCHAR(500) COMMENT '店铺简介',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS foot_traffic (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    date DATE NOT NULL,
    total_passers INT DEFAULT 0,
    total_enter INT DEFAULT 0,
    enter_rate DECIMAL(5,2) DEFAULT 0.00,
    avg_stay_seconds INT DEFAULT 0,
    male_ratio DECIMAL(5,2) DEFAULT 0.00,
    female_ratio DECIMAL(5,2) DEFAULT 0.00,
    peak_hour VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id),
    UNIQUE KEY uk_shop_date (shop_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS content_calendar (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    plan_date DATE NOT NULL,
    content_type VARCHAR(30),
    video_theme VARCHAR(200),
    ai_script TEXT,
    hook_text VARCHAR(200),
    body_text TEXT,
    cta_text VARCHAR(100),
    hashtags VARCHAR(200),
    best_time VARCHAR(20),
    publish_status TINYINT DEFAULT 0,
    published_at DATETIME,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id),
    UNIQUE KEY uk_shop_plan_date (shop_id, plan_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS review_alert (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    platform VARCHAR(30),
    reviewer_name VARCHAR(100),
    rating INT,
    negative_score DECIMAL(5,2) DEFAULT 0.00,
    content TEXT,
    ai_suggestion TEXT,
    ai_reply TEXT,
    reply_status TINYINT DEFAULT 0,
    reply_adopted VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS dashboard_stats (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    stat_date DATE NOT NULL,
    content_views INT DEFAULT 0,
    content_likes INT DEFAULT 0,
    content_comments INT DEFAULT 0,
    content_shares INT DEFAULT 0,
    new_followers INT DEFAULT 0,
    guide_orders INT DEFAULT 0,
    guide_revenue DECIMAL(10,2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shop_id) REFERENCES shop(id),
    UNIQUE KEY uk_shop_stat_date (shop_id, stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 测试数据
INSERT INTO shop (name, category, address, contact, description) VALUES
('老王家常菜', '餐饮', '北京市朝阳区望京街道', '13800138000', '20年地道家常菜，人气爆满'),
('美颜阁美容店', '美业', '上海市静安区南京西路', '13900139000', '专业美容护理，会员制'),
('动杰健身房', '健身房', '广州市天河区天河路', '13700137000', '24小时营业，器械齐全');

INSERT INTO foot_traffic (shop_id, date, total_passers, total_enter, enter_rate, avg_stay_seconds, male_ratio, female_ratio, peak_hour) VALUES
(1, CURDATE()-6, 320, 85, 26.56, 1800, 58.20, 41.80, '11:30,12:30,18:00'),
(1, CURDATE()-5, 380, 102, 26.84, 2100, 55.10, 44.90, '12:00,18:30'),
(1, CURDATE()-4, 290, 78, 26.90, 1650, 60.00, 40.00, '11:00,19:00'),
(1, CURDATE()-3, 410, 115, 28.05, 2400, 52.30, 47.70, '12:00,18:00'),
(1, CURDATE()-2, 450, 128, 28.44, 2700, 54.00, 46.00, '12:00,18:30,19:00'),
(1, CURDATE()-1, 520, 148, 28.46, 3000, 53.50, 46.50, '11:30,12:00,18:00,19:00'),
(1, CURDATE(), 480, 136, 28.33, 2600, 55.00, 45.00, '12:00,18:30');

INSERT INTO content_calendar (shop_id, plan_date, content_type, video_theme, hook_text, body_text, cta_text, hashtags, best_time, publish_status) VALUES
(1, CURDATE(), '种草', '招牌红烧肉', '老板们！这道红烧肉我能吃三碗饭！', '今天揭秘我们后厨的秘密...', '看完记得点赞关注', '#老王家常菜 #红烧肉 #家常菜 #美食', '12:00', 1),
(1, CURDATE()+1, '促销', '周年庆优惠', '周年庆来了，全场8折！', '为感谢新老客户...', '快来门店吧！', '#老王家常菜 #周年庆 #优惠', '19:00', 0),
(1, CURDATE()+2, '展示', '后厨探店', '带你们看看真正的后厨！', '每天新鲜食材，现做现卖...', '关注我，更多探店内容', '#老王家常菜 #后厨 #探店', '18:00', 0);

INSERT INTO review_alert (shop_id, platform, reviewer_name, rating, negative_score, content, ai_suggestion, ai_reply, reply_status) VALUES
(1, 'dianping', '用户小明', 2, 0.80, '等位等了40分钟，菜上来都凉了，服务态度也不好', '建议：主动联系顾客致歉，提供下次消费优惠补偿；同时优化高峰期排队管理', '非常抱歉给您带来不好的体验，我们是20年老店...', 1),
(1, 'meituan', '吃货张三', 1, 0.95, '点的红烧肉明显是预制菜，跟图片差太多，坑人！', '建议：核实食材来源，如确实有问题需立即调整；主动在平台公开回应', '感谢您的反馈，我们一直坚持现做...', 0);