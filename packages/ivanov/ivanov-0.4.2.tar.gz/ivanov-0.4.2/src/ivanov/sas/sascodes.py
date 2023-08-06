from string import Template


class SasCodeTemplate(Template):
    delimiter = '#'


extract_lib_template = SasCodeTemplate("""
%let metasrv="#{metadata_server}";
%let metaprt=#{metadata_port};
%let metausr="#{metadata_user}";
%let metapwd="#{metadata_password}";
%let metarep="#{metadata_repo}";

%macro libsfromrepo(mdrep=);
/*************************************************************/

/*%macro getMetaInfos(EXCELFILE,OUTPUTFORMAT);*/
  data metadata_libraries;
  length uri serveruri conn_uri domainuri conns_uri serv_uri propuri libname ServerContext AuthDomain path_schema
         usingpkguri type tableuri coluri $256 id $17
         desc $200 libref engine $8 isDBMS $1 DomainLogin  $32
		 Server_connection $100 Server_meta $50 TnsODBC $50 TnsODBC2 $50
			repo $50;
  /*keep libname desc libref engine ServerContext path_schema AuthDomain table colname
      coltype collen IsPreassigned IsDBMSLibname id Server_connection Server_meta TnsODBC TnsODBC2;*/
  keep libname desc libref engine ServerContext path_schema AuthDomain  
        IsPreassigned /*IsDBMSLibname*/ /*id*/ Server_connection Server_meta TnsODBC TnsODBC2 repo;

  nobj=.;
  n=1;
  uri='';
  serveruri='';
  conn_uri='';
  domainuri='';

         /***Determine how many libraries there are***/
  nobj=metadata_getnobj("omsobj:SASLibrary?@Id contains '.'",n,uri);
         /***Retrieve the attributes for all libraries, if there are any***/
  if n>0 then do n=1 to nobj;
    libname='';
    ServerContext='';
    AuthDomain='';
    desc='';
    libref='';
    engine='';
    isDBMS='';
    IsPreassigned='';
    IsDBMSLibname='';
    path_schema='';
    usingpkguri='';
    type='';
    id='';
	Server_connection='';
	Server_meta='';
	TnsODBC='';
	TnsODBC2='';

    nobj=metadata_getnobj("omsobj:SASLibrary?@Id contains '.'",n,uri);
    rc= metadata_getattr(uri, "Name", libname);
    rc= metadata_getattr(uri, "Desc", desc);
    rc= metadata_getattr(uri, "Libref", libref);
    rc= metadata_getattr(uri, "Engine", engine);
    rc= metadata_getattr(uri, "IsDBMSLibname", isDBMS);
    rc= metadata_getattr(uri, "IsDBMSLibname", IsDBMSLibname); 
    rc= metadata_getattr(uri, "IsPreassigned", IsPreassigned); 
    rc= metadata_getattr(uri, "Id", Id);

    /*** Get associated ServerContext ***/
    i=1;
    rc= metadata_getnasn(uri, "DeployedComponents", i, serveruri);
    if rc > 0 then rc2= metadata_getattr(serveruri, "Name", ServerContext);
    else ServerContext='';

    /*** If the library is a DBMS library, get the Authentication Domain
         associated with the DBMS connection credentials ***/
    if isDBMS="1" then do;
      i=1; 
      rc= metadata_getnasn(uri, "LibraryConnection", i, conn_uri);
      if rc > 0 then do;
        rc2= metadata_getnasn(conn_uri, "Domain", i, domainuri);
        if rc2 > 0 then do;
			rc3= metadata_getattr(domainuri, "Name", AuthDomain);
			rc4=metadata_getnasn(domainuri, "Connections", i, conns_uri);
			if rc4>0 then do;
				rc4=metadata_getattr(conns_uri, "Name", Server_connection);
				rc5=metadata_getnasn(conns_uri, "Source", i, serv_uri);
				if rc5>0 then do;
					rc5=metadata_getattr(serv_uri, "Name", Server_meta);
				end;
			end;
		end;
		rc2=metadata_getnasn(conn_uri, "Properties", i, propuri);
		if rc2 > 0 then do;
			rc3=metadata_getattr(propuri, "DefaultValue", TnsODBC);
		end;

		rc2_2=metadata_getnasn(conn_uri, "Properties", 2, propuri);
		if rc2_2 > 0 then do;
			rc3=metadata_getattr(propuri, "DefaultValue", TnsODBC2);
		end;

      end;
    end;

    /*** Get the path/database schema for this library ***/
    rc=metadata_getnasn(uri, "UsingPackages", 1, usingpkguri);
    if rc>0 then do;
      rc=metadata_resolve(usingpkguri,type,id);  
      if type='Directory' then 
        rc=metadata_getattr(usingpkguri, "DirectoryName", path_schema);
      else if type='DatabaseSchema' then 
        rc=metadata_getattr(usingpkguri, "SchemaName", path_schema);
      else path_schema="unknown";
    end;
  repo="&mdrep";
  output;
    
  end;
 
 run;

 proc append base=Libraries_final
 	data=metadata_libraries;
%mend;


options /*metaserver="sasmeta.dwhgridprod.imb.ru"*/
		metaserver=&metasrv
        metaport=&metaprt
        metauser=&metausr
        metapass=&metapwd
        metarepository=&metarep;

/*получаем список репозиториев SAS*/


filename myoutput temp;

proc metadata 
out=myoutput
header=full
   in="<GetRepositories>
   <Repositories/> 
   <!-- OMI_ALL (1) flag -->
   <Flags>1</Flags>
    <Options/> 
   </GetRepositories>";
run;


filename getrepos temp;
libname getrepos xmlv2 xmlfileref=myoutput automap=replace xmlmap=getrepos;
proc copy in=getrepos out=work;
run;

proc sql;
	delete from Repository
	where Repository_name in ('REPOSMGR','BILineage');
quit;


data run;
	set Repository;
	str = catt('options metaserver=',&metasrv,' metaport=',&metaprt,' metauser="',&metausr,'" metapass="',&metapwd,'" metarepository="', Repository_Name,'";');
	str_macro = catt('%libsfromrepo(mdrep=', Repository_Name,');');
	call execute(str);
	call execute(str_macro);
run;

proc sql;
	delete from Libraries_final
	where libname ='';
quit;
""")

extract_authdomains_template = SasCodeTemplate("""

proc sql;
create table authdoms
(authdom char(50)
,userid char(50)
,pwencode char(200)
,pwdecode char(200)
,desc char(500)
/*,system char(50)*/);
quit;


%macro Auth(Authdom,UserId,Password,Desc);
	
	proc groovy;
		add sasjar="sas.core";
		eval "import com.sas.util.SasPasswordString; exports.OpenPassword=SasPasswordString.decode(""&Password"")";
	run;

	proc sql inobs=1;
		insert into authdoms
		select "&Authdom.","&UserId.","&Password.","&OpenPassword.","&Desc."
		from sashelp.table;
	quit;
	%let OpenPassword=;
%mend;

%let metasrv="sasmeta.dwhgridprod.imb.ru";
%let metaprt=8561;
/*%let metausr="sasadm@saspw";*/
%let metausr="mb30728";
/*%let metapwd="{SAS002}FACB520F2A1764C93DD09B70191005080290E78A";*/
%let metapwd="{SAS002}";
%let metarep="Foundation";

options 
		metaserver=&metasrv
        metaport=&metaprt
        metauser=&metausr
        metapass=&metapwd
        metarepository=&metarep;

/*************************************************************/
  data metadata_authdomains;
  length uri authdom desc outbound loginuri userid password AuthId openpassword$256 ;
  keep authdom desc outbound userid password openpassword;
  nobj=0;
  n=1;
  uri='';
         /***Determine how many authdom there are***/
  nobj=metadata_getnobj("omsobj:AuthenticationDomain?@Id contains '.'",n,uri);
         /***Retrieve the attributes for all libraries, if there are any***/
  if n>0 then do n=1 to nobj;
	AuthId='';
	authdom='';
	desc='';
	outbound='';
	loginuri='';
	UserID='';
	Password='';

    nobj=metadata_getnobj("omsobj:AuthenticationDomain?@Id contains '.'",n,uri);
	rc= metadata_getattr(uri,"Id",AuthId);
    rc= metadata_getattr(uri, "Name", authdom);
    rc= metadata_getattr(uri, "Desc", desc);
    rc= metadata_getattr(uri, "OutboundOnly", outbound);

	rc=1;
    tn=1;
	nobj2=0;

	nobj2=metadata_getnasn("OMSOBJ:AuthenticationDomain\"!!AuthId,"Logins",tn,loginuri);
	if nobj2<0 then do; output; end;
	do tn=1 to nobj2;
 	   rc=metadata_getnasn("OMSOBJ:AuthenticationDomain\"!!AuthId,"Logins",tn,loginuri);
  	   if rc>0 then do;
   	     rc2=metadata_getattr(loginuri,"UserID",UserID);
    	 rc2=metadata_getattr(loginuri,"Password",Password);
		 output;
		 UserID='';
		 Password=''; 
       end;
    end;
  end;
 run;


data run;
	set metadata_authdomains;
	str_macro = catt('%Auth(', authdom,',', userid,',',password,',',desc,');');
	call execute(str_macro);
run;


data _null_;
	set run;
	call execute(str_macro);
run;

                                                """)

