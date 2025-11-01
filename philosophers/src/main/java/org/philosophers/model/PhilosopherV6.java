package org.philosophers.model;

import java.time.Duration;
import java.time.Instant;

public class PhilosopherV6 extends PhilosopherBase {
    public static final String BASE_DIR = "src/main/resources/version6/";
    private final Waiter waiter;

    public PhilosopherV6(Fork left, Fork right, int id, String filename, Waiter waiter) {
        super(left, right, id, BASE_DIR + filename);
        this.waiter = waiter;
    }

    @Override
    protected void eat() {
        Instant start;
        long waitingTime;
        boolean ateOnCorridor;

        if (!waiter.isDiningHallFull()) {
            ateOnCorridor = true;
            System.out.println("Philosopher " + this.id + " was escorted out of the dining room");

            start = Instant.now();
            right.lift();
            System.out.println("Philosopher " + this.id + " lifted right fork (" + this.right.getId() + ")");

            left.lift();
            waitingTime = Duration.between(start, Instant.now()).toMillis();
            System.out.println("Philosopher " + this.id + " lifted left fork (" + this.left.getId() + ")");
        } else {
            ateOnCorridor = false;
            start = Instant.now();
            waiter.makeOrder();

            left.lift();
            System.out.println("Philosopher " + this.id + " lifted left fork (" + this.left.getId() + ")");

            right.lift();
            waitingTime = Duration.between(start, Instant.now()).toMillis();
            System.out.println("Philosopher " + this.id + " lifted right fork (" + this.right.getId() + ")");
        }
        System.out.println("Philosopher " + this.id + " lifted both forks (" + this.left.getId() + " and " + this.right.getId() + ")");

        finishEating();
        if (!ateOnCorridor) {
            waiter.askForReceipt();
        }
        writeLineCsv(String.valueOf(waitingTime), true);
    }
}
