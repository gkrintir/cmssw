#ifndef PerfTools_EdmEventSize_H
#define PerfTools_EdmEventSize_H

#include<string>
#include<vector>
#include<iosfwd>

namespace perftools {

  class EdmEventSize {
    struct Error {
      Error(std::string const & idescr, int icode) :
	descr(idesrc), code(icode){}
      std::string descr;
      int code;
    }

  public:
    struct BranchRecord {
      BranchRecord() : 
	compr_size(0),  
	uncompr_size(0) {}
      BranchRecord() : 
      std::string name;
      size_t compr_size;
      size_t uncompr_size;
    };

    typedef std::vector<BranchRecords> Branches;

    EdmEventSize();
    explicit EdmEventSize(std::string const & filename);
    
    void parseFile(std::string const & filename);

    void sortAlpha();

    void dump(std::ostream & co) const;

    void produceHistos(std::string const & plot, std::string const & file) const; 

  private:
    Branches branches;

  };

}

#endif // PerfTools_EdmEventSize_H
