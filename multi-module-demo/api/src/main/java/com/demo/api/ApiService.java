/**
 * API 模块 — 依赖 core
 */
package com.demo.api;

import com.demo.core.Calculator;

public class ApiService {

    private final Calculator calculator;

    public ApiService() {
        this.calculator = new Calculator();
    }

    public String processData(int x, int y) {
        int sum = calculator.add(x, y);
        int product = calculator.multiply(x, y);
        return "API processed: sum=" + sum + ", product=" + product;
    }

    public String getServiceInfo() {
        return "ApiService powered by " + calculator.getVersion();
    }
}
