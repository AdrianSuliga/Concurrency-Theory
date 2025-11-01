package org.philosophers.simulation;

import org.philosophers.model.*;

import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.List;

public class Simulation<PhilosopherType extends PhilosopherBase> {
    private final Waiter waiter;
    private final List<PhilosopherType> philosophers;
    private final Fork[] forks;

    public Simulation(int n, Class<PhilosopherType> clazz) {
        this.waiter = new Waiter(n - 1);
        this.forks = new Fork[n];
        this.philosophers = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            forks[i] = new Fork(i + 1);
        }

        try {
            if (clazz.equals(PhilosopherV5.class) || clazz.equals(PhilosopherV6.class)) {
                Constructor<PhilosopherType> constructor = clazz.getConstructor(
                        Fork.class, Fork.class, int.class, String.class, Waiter.class
                );

                for (int i = 0; i < n; i++) {
                    philosophers.add(constructor.newInstance(forks[i], forks[(i + 1) % n], i + 1, n + "_philosophers/philosopher_n" + (i + 1) + ".csv", waiter));
                }
            } else {
                Constructor<PhilosopherType> constructor = clazz.getConstructor(
                        Fork.class, Fork.class, int.class, String.class
                );

                for (int i = 0; i < n; i++) {
                    philosophers.add(constructor.newInstance(forks[i], forks[(i + 1) % n], i + 1, n + "_philosophers/philosopher_n" + (i + 1) + ".csv"));
                }
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void simulate() {
        philosophers.forEach(Thread::start);
        philosophers.forEach(pThread -> {
            try {
                pThread.join();
            } catch (InterruptedException e) {
                System.out.println(e.getMessage());
            }
        });
    }
}
