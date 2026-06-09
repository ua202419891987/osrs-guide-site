package com.example.gradle;

import org.gradle.api.Plugin;
import org.gradle.api.Project;

public class DemoPlugin implements Plugin<Project> {
    @Override
    public void apply(Project project) {
        // 创建一个任务
        project.getTasks().register("helloDemo", task -> {
            task.doLast(t -> System.out.println("Hello from Demo Gradle Plugin!"));
        });
        
        // 打印日志
        project.getLogger().quiet("Demo Plugin applied to project: " + project.getName());
    }
}
