# Force-Calculator
The problem: If P stationary charges are randomly laid out on an NxN finite plane and randomly assigned charges of +1 or -1, what is the magnitude of the force felt throughout the field according to Coulomb’s Law?

My solution: The code solves for the electromagnetic force at each coordinate in an NxN matrix from each point charge. The matrices are added together until there is one NxN matrix of the magnitude of the net force felt at each point. Each point is plotted at the coordinates of its position in the matrix. The color of the point is red if the force magnitude is positive and blue if it is negative. The size of each point is scaled with the magnitude of the force.

Some further steps I could take:
 - Choosing charges that are not just +1 or -1
 - Modeling this problem in three dimensions
 - Observing how the particles would move over time
