package org.philosophers.model;

import java.time.Duration;
import java.time.Instant;

public class PhilosopherV5 extends PhilosopherBase {
    private static final String BASE_DIR = "src/main/resources/version5/";
    private final Waiter waiter;

    public PhilosopherV5(Fork left, Fork right, int id, String filename, Waiter waiter) {
        super(left, right, id, BASE_DIR + filename);
        this.waiter = waiter;
    }

    @Override
    protected void eat() {
        Instant start = Instant.now();

        waiter.makeOrder();
        left.lift();
        System.out.println("Philosopher " + this.id + " lifted left fork (" + this.left.getId() + ")");

        right.lift();
        System.out.println("Philosopher " + this.id + " lifted right fork (" + this.right.getId() + ")");

        long timeElapsed = Duration.between(start, Instant.now()).toMillis();

        finishEating();
        waiter.askForReceipt();
        writeLineCsv(String.valueOf(timeElapsed), true);
    }

}
