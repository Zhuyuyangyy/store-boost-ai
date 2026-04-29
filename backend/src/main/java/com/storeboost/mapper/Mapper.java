package com.storeboost.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.storeboost.entity.*;
import org.apache.ibatis.annotations.*;

public interface ShopMapper extends BaseMapper<Shop> {}

public interface FootTrafficMapper extends BaseMapper<FootTraffic> {}

public interface ContentCalendarMapper extends BaseMapper<ContentCalendar> {}

public interface ReviewAlertMapper extends BaseMapper<ReviewAlert> {}

public interface DashboardStatsMapper extends BaseMapper<DashboardStats> {}