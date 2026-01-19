package com.legacy.modernizer;

import com.legacy.modernizer.model.User;

public class Main {
    public static void main(String[] args) {
        System.out.println("Legacy Application Started");

        Object response = "Hello, World!";

        switch (response) {
            case String s -> System.out.println("Result is a string: " + s);
            case Integer i -> System.out.println("Result is a number: " + i);
            case null, default -> {}
        }

        var user = new User("123", "test@example.com");
        System.out.println("User ID: " + user.id());
        System.out.println("User Email: " + user.email());
    }
}