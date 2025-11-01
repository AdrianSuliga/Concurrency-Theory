package org.philosophers.model;

import java.time.Duration;
import java.time.Instant;

public class PhilosopherV1 extends PhilosopherBase {
    public static final String BASE_DIR = "src/main/resources/version1/";

    public PhilosopherV1(Fork left, Fork right, int id, String filename) {
        super(left, right, id, BASE_DIR + filename);
    }

    @Override
    protected void eat() {
        Instant start = Instant.now();
        this.left.lift();
        System.out.println("Philosopher " + this.id + " lifts left fork (" + this.left.getId() + ")");

        this.right.lift();
        long timeElapsed = Duration.between(start, Instant.now()).toMillis();
        System.out.println("Philosopher " + this.id + " lifts right fork (" + this.right.getId() + ")");

        finishEating();
        writeLineCsv(String.valueOf(timeElapsed), true);
    }
}
