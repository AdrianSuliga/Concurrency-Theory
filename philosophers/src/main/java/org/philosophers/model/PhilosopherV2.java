package org.philosophers.model;

import java.time.Duration;
import java.time.Instant;

public class PhilosopherV2 extends PhilosopherBase {
    public static final String BASE_DIR = "src/main/resources/version2/";

    public PhilosopherV2(Fork left, Fork right, int id, String filename) {
        super(left, right, id, BASE_DIR + filename);
    }

    @Override
    protected void eat() {
        Instant start = Instant.now();
        while (left.isLifted() || right.isLifted()) {
            think();
        }

        this.left.lift();
        this.right.lift();

        long timeElapsed = Duration.between(start, Instant.now()).toMillis();

        System.out.println("Philosopher " + this.id + " lifted both forks (" + this.left.getId() + " and " + this.right.getId() + ")");

        finishEating();
        writeLineCsv(String.valueOf(timeElapsed), true);
    }

}
