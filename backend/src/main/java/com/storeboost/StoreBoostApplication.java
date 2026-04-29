package com.storeboost;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.storeboost.mapper")
public class StoreBoostApplication {
    public static void main(String[] args) {
        SpringApplication.run(StoreBoostApplication.class, args);
    }
}