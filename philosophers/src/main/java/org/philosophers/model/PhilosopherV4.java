package org.philosophers.model;

import java.time.Duration;
import java.time.Instant;

public class PhilosopherV4 extends PhilosopherBase {
    public static final String BASE_DIR = "src/main/resources/version4/";

    public PhilosopherV4(Fork left, Fork right, int id, String filename) {
        super(left, right, id, BASE_DIR + filename);
    }

    @Override
    protected void eat() {
        Instant start = Instant.now();

        if (Math.random() < 0.5) {
            right.lift();
            System.out.println("Philosopher " + this.id + " lifted right fork (" + this.right.getId() + ")");

            left.lift();
            System.out.println("Philosopher" + this.id + " lifted left fork (" + this.left.getId() + ")");
        } else {
            left.lift();
            System.out.println("Philosopher " + this.id + " lifted left fork (" + this.left.getId() + ")");

            right.lift();
            System.out.println("Philosopher " + this.id + " lifted right fork (" + this.right.getId() + ")");
        }

        long timeElapsed = Duration.between(start, Instant.now()).toMillis();

        finishEating();
        writeLineCsv(String.valueOf(timeElapsed), true);
    }
}
