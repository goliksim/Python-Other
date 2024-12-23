#created by goliksim on 27 apr 2023

import numpy as np
from scipy.spatial import ConvexHull        #pip install scikit-learn
from itertools import combinations
    #pip install shapely
import cdd as pcdd                          #pip install pycddlib


def intersect3D_SegmentPlane(Segment, Plane):

    # Points in Segment: Pn  Points in Plane: Qn
    P0, P1     = np.array(Segment.coords)
    Q0, Q1, Q2 = Plane   

    # vectors in Plane
    q1 = Q1 - Q0
    q2 = Q2 - Q0

    # vector normal to Plane
    n  = np.cross(q1, q2)/np.linalg.norm(np.cross(q1, q2))
    u = P1 - P0 # Segment's direction vector 
    w = P0 - Q0 # vector from plane ref point to segment ref point

    ## Tests parallelism
    if np.dot(n, u) == 0:
        print ("Segment and plane are parallel")
        print ("Either Segment is entirely in Plane or they never intersect.")
        return None
    ## if intersection is a point
    else:
        ## Si is the scalar where P(Si) = P0 + Si*u lies in Plane
        Si = np.dot(-n, w) / np.dot(n, u)
        PSi = P0 + Si * u
        return PSi

def in_poly_hull_single(poly, point):
    hull = ConvexHull(poly)
    new_hull = ConvexHull(np.concatenate((poly, [point])))
    return np.array_equal(new_hull.vertices, hull.vertices)

def get_clean_points(matrix):
    N = len(matrix)
    vertices = np.hstack((np.ones((N,1)), matrix)) # to get the convex hull with cdd one needs to add a unit column
    mat = pcdd.Matrix(vertices, linear=False, number_type="fraction") # make a polyhedron
    mat.rep_type = pcdd.RepType.GENERATOR

    poly = pcdd.Polyhedron(mat)
    adjacencies = [list(x) for x in poly.get_input_adjacency()] # get neighboring vertices of each vertex
    return [index for index, vert in enumerate(adjacencies) if len(vert)!=0], adjacencies

def find_intersection(clean_points, pts,adj, line):
    intersections = []
    for i in list(combinations(clean_points, 3)):
        if (i[1] in adj[i[0]] and i[2] in adj[i[0]] and i[1] in adj[i[2]]):
            # intersection point of a plane of three points and a bisector
            intersect = intersect3D_SegmentPlane(line, pts[i,:])  
            try:
                if (in_poly_hull_single(pts, intersect)): # checking that a point is in polygon
                    intersections.append(list(intersect))
            except:
                pass
    intersections =   np.unique(intersections,axis = 0)
    if len(intersections)>=2:
        intersections = np.array([intersections[0],intersections[-1]])
    return intersections

def plot_projection(ax,intersections, start = 0):
    ax.plot([intersections[0,0],intersections[0,0]],[intersections[0,1],intersections[0,1]],[intersections[0,2],start], c = 'g')
    ax.plot([intersections[0,0],start],[intersections[0,1],intersections[0,1]],[start,start], c = 'g', linestyle= ":")
    ax.plot([intersections[0,0],intersections[0,0]],[intersections[0,1],0],[start,start], c = 'g', linestyle= ":")
    ax.text(intersections[0,0],intersections[0,1],start, "cr={:.2f}".format(intersections[0][0]))

def plot_edges(adjacencies, ax, points):
    N = len(adjacencies)    
    # store the edges in a matrix (giving the indices of the points)
    edges = [None]*(N-1)
    for i,indices in enumerate(adjacencies[:-1]):
        indices = list(filter(lambda x: x>i, indices))
        l = len(indices)
        col1 = np.full((l, 1), i)

        indices = np.reshape(indices, (l, 1))
        
        edges[i] = np.hstack((col1, indices))
    Edges = np.vstack(tuple(edges))
    Edges = Edges.astype(int)
    start = points[Edges[:,0]]
    end = points[Edges[:,1]]
    for i in range(len(end)):
        ax.plot(
            [start[i,0], end[i,0]], 
            [start[i,1], end[i,1]], 
            [start[i,2], end[i,2]],
            "blue"
        )
    
def find_random_square(points, ax,min_max_risk):
    vertices = np.hstack((np.ones((len(points),1)), points)) # to get the convex hull with cdd one needs to add a unit column
    mat = pcdd.Matrix(vertices, linear=False, number_type="fraction") # make a polyhedron
    poly1 = pcdd.Polyhedron(mat)
    h1 = poly1.get_inequalities()


    steps = np.linspace(min_max_risk,0.1,5000)
    for index, step in enumerate(steps):
        cube = [(step, 0, 0), (step, step, 0), (step, step,step), (step, 0,step),(0, step, 0),(0, step,step),(0, 0, step), (step, 0, step)]
        vertices = np.hstack((np.ones((len(cube),1)), cube)) # to get the convex hull with cdd one needs to add a unit column
        mat = pcdd.Matrix(vertices, linear=False, number_type="fraction") # make a polyhedron
        poly2 = pcdd.Polyhedron(mat)
        h2 = poly2.get_inequalities()
        hintersection = np.vstack((h1, h2))
        mat = pcdd.Matrix(hintersection, number_type='fraction')
        mat.rep_type = pcdd.RepType.INEQUALITY
        polyintersection = pcdd.Polyhedron(mat)
        vintersection = polyintersection.get_generators()
        if vintersection.row_size == 0 :
            break
        
    random_risk = steps[index-1]

    ax.plot([random_risk,random_risk],[random_risk,0],[random_risk,random_risk], c ='g')
    ax.plot([random_risk,0],[random_risk,random_risk],[random_risk,random_risk], c ='g')
    ax.plot([random_risk,random_risk],[random_risk,random_risk],[random_risk,0], c ='g')
    ax.text(random_risk*0.8,random_risk*0.8, 0 ,"cb_r={:.2f}".format(random_risk))
    ax.plot([random_risk,0],[random_risk,random_risk],[0,0], c = 'g', linestyle= ":")
    ax.plot([random_risk,random_risk],[random_risk,0],[0,0], c = 'g', linestyle= ":")
    print(f"Рандомизированный риск методом куба: "+ "{:.2f}".format(random_risk))

    return random_risk
    
    
