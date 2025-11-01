package org.philosophers;

import org.philosophers.model.PhilosopherV1;
import org.philosophers.model.PhilosopherV2;
import org.philosophers.model.PhilosopherV3;
import org.philosophers.model.PhilosopherV4;
import org.philosophers.model.PhilosopherV5;
import org.philosophers.model.PhilosopherV6;
import org.philosophers.simulation.*;
import org.philosophers.utils.GraphGenerator;

public class Main {
    public static void main() {

        /* Example simulation with N philosophers executing variant 6
        int N = 20;

        var simulation = new Simulation<>(N, PhilosopherV6.class);
        simulation.simulate();
         */

        /* Generate graph for average times for all variant 6 philosophers, graph generation assumes Ns to be 5, 10, 15 or 20
        GraphGenerator graph = new GraphGenerator();

        for (int i = 5; i < 21; i += 5) {
            graph.generateForNPhilosophers(PhilosopherV6.BASE_DIR, i);
        }
        */

        /* Generate summary graph for all variants */
        GraphGenerator graph = new GraphGenerator();
        graph.generateForAllVariants();
    }
}
