package com.legacy.modernizer.model;

public class User {
    private final String id;
    private final String email;

    public User(String id, String email) {
        // Validation before super() - This is the "Flexible Constructor" test
        if (id == null || email == null) {
            throw new IllegalArgumentException("Fields cannot be null");
        }
        this.id = id;
        this.email = email;
    }

    public String getId() { return id; }
    public String getEmail() { return email; }

    @Override
    public String toString() {
        return "User{id='" + id + "', email='" + email + "'}";
    }
}
