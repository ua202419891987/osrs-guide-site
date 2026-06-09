/**
 * Core 模块 — 共享工具库
 * 不依赖任何其他模块
 */
package com.demo.core;

public class Calculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public String getVersion() {
        return "Core v1.0";
    }
}
