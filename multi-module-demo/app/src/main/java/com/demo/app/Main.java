/**
 * App 模块 — 主应用入口
 * 依赖 core + api
 */
package com.demo.app;

import com.demo.core.Calculator;
import com.demo.api.ApiService;

public class Main {
    public static void main(String[] args) {
        // 直接使用 core
        Calculator calc = new Calculator();
        System.out.println("Core: 3 + 4 = " + calc.add(3, 4));
        System.out.println("Core: " + calc.getVersion());

        // 使用 api（内部也调用了 core）
        ApiService api = new ApiService();
        System.out.println(api.getServiceInfo());
        System.out.println(api.processData(5, 6));

        System.out.println("\n✅ 多模块项目跑通了！");
    }
}
