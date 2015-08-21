// C routine to read CUBE file

#include<Python.h>
#include <numpy/arrayobject.h>

void readCubeHeader(char *inp, 
                   double **structure,
                   double **grid,
                   int dims[3], int size[2])
{
  FILE *fr;
  int Na, N3=1;
  double read;
  int i, j=0;
  char *string = (char *) malloc(80);
  size_t len=0;

  // CUBE file contains fixed size grid specification
  *grid = (double *) malloc(16 * sizeof(double));

  fr = fopen(inp, "r");
  for(i=0;i<2;i++){
    getline(&string, &len, fr);
  }

  for(i=0;i<16;i++){
    fscanf(fr, "%lf", &read);
    (*grid)[i] = read;
  }
  getline(&string, &len, fr);

  // assign proper value to related parameters
  Na = (*grid)[0];
  size[0] = Na;
  size[1] = 4;
  for(i=0;i<3;i++){
    dims[i] = (int) (*grid)[4 * (i+1)];
    N3 *= dims[i];
  }

  *structure = (double *) malloc(4 * Na * sizeof(double));

  for(i=0;i<Na*5;i++){
    fscanf(fr, "%lf", &read);
    if((i%5) != 0){
      (*structure)[j++] = read;
    }
  }
  fclose(fr);
  free(string);
}



/////////////////////////////////////////
// main function for reading CUBE file //
/////////////////////////////////////////
// or what ever computation need to be done
// only minor changes should be necessary
// to interface other type of calculation
void readcube_c(char *inp, 
                double *cube, 
                double *structure, 
                double *grid, 
                int dims[3],
                int size[2])
{
  FILE *fr;
  int Na, N3=1;
  double read;
  int i, j=0;
  char *string = (char *) malloc(80);
  size_t len=0;

  // CUBE file contains fixed size grid specification
//  *grid = (double *) malloc(16 * sizeof(double));

  fr = fopen(inp, "r");
  for(i=0;i<2;i++){
    getline(&string, &len, fr);
  }

  for(i=0;i<16;i++){
    fscanf(fr, "%lf", &read);
    grid[i] = read;
  }
  getline(&string, &len, fr);

  // assign proper value to related parameters
  Na = grid[0];
  size[0] = Na;
  size[1] = 4;
  for(i=0;i<3;i++){
    dims[i] = (int) grid[4 * (i+1)];
    N3 *= dims[i];
  }

//  *structure = (double *) malloc(4 * Na * sizeof(double));
//  *cube = (double *) malloc(N3 * sizeof(double));

  for(i=0;i<Na*5;i++){
    fscanf(fr, "%lf", &read);
    if((i%5) != 0){
      structure[j++] = read;
    }
  }

  // check extra line for molecular orbital index
  // signiture of corner wavefunction/density 
  // value is always a small
  fscanf(fr, "%lf", &read);
  if((read>0) && (read<1.0E-4)){
    // i.e. without MO index
    cube[0] = read;
    j=1;
  }else{
    // with MO index
    getline(&string, &len, fr);
    j=0;
  }

  for(i=j;i<N3;i++){
    if(!feof(fr)){
      fscanf(fr,"%le", &read);
      cube[i] = read;
    }else{
      // check for incomplete CUBE file
      printf("end of file at i=%d\n",i-1);
      break;
    }
  }

  fclose(fr);
  free(string);
}

//////////////////////////////////////////////
// redirect PyArray data contant to C-array //
//////////////////////////////////////////////
//void Carr2pyarr(double *carrin,
//                int dims[],
//                int nd,
//                PyArrayObject **pyout)
//{
//  int i, N=1;
//
//  *pyout = (PyArrayObject*) PyArray_FromDims(nd, dims, NPY_DOUBLE);
//
//  for(i=0;i<nd;i++){
//    N *= dims[i];
//  }
//  
//  for(i=0;i<N;i++){
//    (*pyout)->data[i] = carrin[i];
//    printf("%lf->%lf\n", (*pyout)->data[i], carrin[i]);
//  }
//}

//double **pymatrix_to_Carrayptrs(PyArrayObject *arrayin) { 
//  double **c, *a;
//  int i,n,m;
// 
//  n=arrayin->dimensions[0];
//  m=arrayin->dimensions[1];
//  c=ptrvector(n);
//  /* pointer to arrayin data as double */
//  a=(double *) arrayin->data; 
//  for ( i=0; i<n; i++) {
//    /* assigning address */
//    c[i]=a+i*m;
//  }
//  return c;
//}
//
//double **ptrvector(long n)  {
//  double **v;
//  v=(double **)malloc((size_t) (n*sizeof(double)));
////  if (!v)   {
////    printf("In **ptrvector. Allocation of memory for double array failed.");
////    exit(0);  }
//  return v;
//}
//
//void free_Carrayptrs(double **v)  {
//  free((char*) v);
//}

double *pyvector_to_Carrayptrs(PyArrayObject *arrayin)  {
  int n=arrayin->dimensions[0];
  /* pointer to arrayin data as double */
  return (double *) arrayin->data;
}

///////////////////////////////////////
// !!! PYTHON INTERFACE FROM HERE!!! //
///////////////////////////////////////

//////////////////////////////
// python callable function //
//////////////////////////////
// input: string, for file name
// output: PyArrayObject, as volumetric data
static PyObject * read_cube(PyObject * self, PyObject * args){
  char *input; // filename string as input
  double *data; // C-data need to be converted to numpy object
  double *structure; // C-data need to be converted to numpy object
  double *grid; // C-data need to be converted to numpy object
  int dims[3], size[2], gsize[2]={4,4};
  int N3=1, i;

  // interface
  // numpy object pass back to python
  PyArrayObject *npdata, *npstructure, *npgrid; 

  // parse arguments check and/or error handling
  if(!PyArg_ParseTuple(args, "s", &input))
    return NULL;

  // run the actual function
  // NOTE the data is passed as datatype double**
  // to allocate memory in the function
  readCubeHeader(input, &structure, &grid, dims, size);

  npdata = (PyArrayObject*) PyArray_FromDims(3, dims, NPY_DOUBLE);
  npstructure = (PyArrayObject*) PyArray_FromDims(2, 
                                   size, NPY_DOUBLE);
  npgrid = (PyArrayObject*) PyArray_FromDims(2, gsize, NPY_DOUBLE);

  for(i=0;i<3;i++) N3 *= dims[i];
  data = (double*) malloc(N3*sizeof(double));

  data = pyvector_to_Carrayptrs(npdata);
  structure = pyvector_to_Carrayptrs(npstructure);
  grid = pyvector_to_Carrayptrs(npgrid);
  readcube_c(input, data, structure, grid, dims, size);

  // numpy C-API: allocate memory to copy C-array data
  // Assume 1-D C-array, N-D numpy array will be filled as
  // [data[0]         : data[dims[0]], 
  //  data[dims[0]+1] : data[dims[1]],
  //  data[dims[1]+1] : data[dims[2]],
  //                 .......             ,
  // ]
//  npdata = PyArray_SimpleNewFromData(3, dims, NPY_DOUBLE, data);
//  npstructure = PyArray_SimpleNewFromData(2, 
//                                          size,
//                                          NPY_DOUBLE,
//                                          structure);
//  npgrid = PyArray_SimpleNewFromData(2, gsize, NPY_DOUBLE, grid);

//  Carr2pyarr(data, dims, 3, &npdata);
//  Carr2pyarr(structure, size, 2, &npstructure);
//  Carr2pyarr(grid, gsize, 2, &npgrid);
  
//  data = pyvector_to_Carrayptrs(npdata);
//  structure = pyvector_to_Carrayptrs(npstructure);
//  grid = pyvector_to_Carrayptrs(npgrid);

//  free(data);
//  free(grid);
//  free(structure);

  return Py_BuildValue("OOO", npdata, npstructure, npgrid);
}

/////////////////////////////////////////
// register python module symbol table //
/////////////////////////////////////////
// PyMethodDef: struct of four field
//   string: method_name
//   PyCFunction: method_function
//   int: flag
//   string: documentation
static PyMethodDef ReadCubeMethods[] = {
  {"read_cube", read_cube, METH_VARARGS, "read CUBE file"},
  {NULL, NULL, 0, NULL} // sentinel?
};

//////////////////////////
//  method constructor  //
//////////////////////////
// the name MUST be init{name} otherwise python cannot find it
// depends on numpy C-API, import_array()
// and/or import_ufunc() are necessary
// otherwise the code return segfault
PyMODINIT_FUNC initread_cube(void){
  Py_InitModule("read_cube", ReadCubeMethods);
  import_array(); // necessary!
}
