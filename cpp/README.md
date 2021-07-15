# C++ Library for the OMEGA Format for Reference Data
This is the C++ counterpart to the python package.
## Usage
```c++
#include <ReferenceRecording.h>

int main(){
    boost::filesystem::path path = boost::filesystem::system_complete("<path to the hdf5 file>");

    std::cout << "Reading from hdf5 file..." << std::endl;
    omega::ReferenceRecording ref_rec = omega::ReferenceRecording::from_hdf5(path.string());

    std::cout << "Writing to hdf5 file..." << std::endl;
    ref_rec.to_hdf5("<path to destination");
}
```

## Build the library

### Requirements (H5cpp)
To create an hdf5 file, the library libhdf5-dev is required.
There are a couple of options to install it.
The following initializes the apt system and installs version 0.4.
This is an old version but provides all feature used in this project.
```
curl http://repos.pni-hdri.de/debian_repo.pub.gpg | sudo apt-key add - 
wget http://repos.pni-hdri.de/focal-pni-hdri.list
sudo cp ./focal-pni-hdri.list /etc/apt/sources.list.d/
sudo apt-get update
sudo apt-get install libh5cpp0.4.0 libh5cpp0.4.0-dbg libh5cpp0.4.0-doc libh5cpp0.4.0-dev
```

### Building
To build the library run `./build.sh`.


