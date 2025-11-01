package org.philosophers.model;

import java.util.concurrent.Semaphore;

public class Fork {
    private final Semaphore semaphore = new Semaphore(1);
    private final int id;

    public Fork(int id) {
        this.id = id;
    }

    public boolean isLifted() {
        return semaphore.availablePermits() == 0;
    }

    public void lift() {
        try {
            semaphore.acquire();
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }

    public void putDown() {
        semaphore.release();
    }

    public int getId() {
        return id;
    }
}
