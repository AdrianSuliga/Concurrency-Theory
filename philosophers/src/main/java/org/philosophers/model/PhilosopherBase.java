package org.philosophers.model;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public abstract class PhilosopherBase extends Thread {
    protected final File csvFile;
    protected final Fork left;
    protected final Fork right;
    protected final int id;

    public PhilosopherBase(Fork left, Fork right, int id, String filename) {
        this.left = left;
        this.right = right;
        this.id = id;
        this.csvFile = new File(filename);

        this.csvFile.getParentFile().mkdirs();
        writeLineCsv("Time [ms]", false);
    }

    protected void think() {
        System.out.println("Philosopher " + this.id + " is thinking.");
        try {
            Thread.sleep((long)(Math.random() * 1000));
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }

    abstract protected void eat();

    protected void finishEating() {
        System.out.println("Philosopher " + this.id + " is eating.");

        try {
            Thread.sleep((long)(Math.random() * 1000));
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }

        left.putDown();
        right.putDown();
    }

    @Override
    public void run() {
        while (true) {
            think();
            eat();
        }
    }

    protected void writeLineCsv(String line, boolean append) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(csvFile, append))) {
            writer.write(line);
            writer.newLine();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
