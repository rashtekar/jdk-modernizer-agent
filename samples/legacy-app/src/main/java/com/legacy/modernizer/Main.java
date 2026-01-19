package com.legacy.modernizer;

import com.legacy.modernizer.model.User;

public class Main {
    public static void main(String[] args) {
        System.out.println("Legacy Application Started");

        Object response = "Hello, World!";

        if (response instanceof String s) {
            System.out.println("Result is a string: " + s);
        } else if (response instanceof Integer i) {
            System.out.println("Result is a number: " + i);
        }

        User user = new User("123", "test@example.com");
        System.out.println("User ID: " + user.getId());
        System.out.println("User Email: " + user.getEmail());
    }
}