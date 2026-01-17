package com.legacy.modernizer;

import com.legacy.modernizer.model.User;

/**
 * This class uses the old way of defining a POJO which the agent should modernize into Record in Java 25.
 */

public class Main {
    public static void main(String[] args) {
        System.out.println("Legacy Application Started");

        Object response = "Hello, World!";

        if (response instanceof String s) {
            System.out.println("Result is a String: " + s);
        } else if (response instanceof Integer i) {
            System.out.println("Result is an Integer: " + i);
        } else {
            System.out.println("Result is of unknown type");
        }

        // Using legacy POJO, agent should modernize this to Record
        User user = new User("123", "test@example.com");
        System.out.println("User ID: " + user.getId());
        System.out.println("User Email: " + user.getEmail());
    }
}