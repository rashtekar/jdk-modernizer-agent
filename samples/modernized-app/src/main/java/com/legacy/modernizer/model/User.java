package com.legacy.modernizer.model;

public record User(String id, String email) {
    public User {
        if (id == null || email == null) {
            throw new IllegalArgumentException("Fields cannot be null");
        }
    }

    @Override
    public String toString() {
        return "User{id='" + id + "', email='" + email + "'}";
    }
}