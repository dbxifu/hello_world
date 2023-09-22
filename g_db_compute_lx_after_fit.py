import db_tools as dt
from db_def_classes_v1 import *
#filter_pha_files_in,continuum_model_in,out_pkl_file,path_pha_in,out_pkl_file,path_data_for_publication=db_select_data_to_look_at()

sname_array=glob.glob("NICER_*.yml")
sname_array_menu=[x.replace("NICER_","").replace(".yml","") for x in glob.glob("NICER_*.yml")]
ind_sname,sname=dt.db_tools_select_an_option_from_menu(sname_array_menu)
print("sname=",sname)
input("Enter")
current_working_directory = os.getcwd()
yml_file=current_working_directory+"/"+sname_array[ind_sname]
root_path_data_for_publication=dyt.db_read_yml(yml_file,"root_path_data_for_publication")
filter_pha_files_in,continuum_model_in,pkl_file_out=dt.db_select_pha_and_model_and_generate_pkl_file_name()
dt.db_print_message("pkl file name should be someting like = "+pkl_file_out)
print(root_path_data_for_publication+sname+"/*"+pkl_file_out)
print(glob.glob(root_path_data_for_publication+sname+"/*/"+pkl_file_out))
include_systematic_errors=click.confirm("\nInclude systematic errors ?", default=True)

#pkl_file_to_read,pkl_file_to_read_without_path_obs=dt.db_tools_list_options_and_select_one_v1(root_path_data_for_publication+sname+"/*/"+pkl_file_out.replace(".pkl",".pkl"))
ind_persistent_lum,persistent_lum=dt.db_tools_select_an_option_from_menu(["Persistent emission luminosity","Burst luminosity"])
if ind_persistent_lum == 0 :
    if include_systematic_errors : pkl_file_to_read_list,pkl_file_to_read_without_path_obs_list=dt.db_tools_list_options_and_select_one_or_all_v0(root_path_data_for_publication+sname+"/*/"+pkl_file_out.replace(".pkl","_persistent.pkl"))
    if not include_systematic_errors : pkl_file_to_read_list,pkl_file_to_read_without_path_obs_list=dt.db_tools_list_options_and_select_one_or_all_v0(root_path_data_for_publication+sname+"/*/"+pkl_file_out.replace(".pkl","_no_sys_persistent.pkl"))
else :
    if include_systematic_errors : pkl_file_to_read_list,pkl_file_to_read_without_path_obs_list=dt.db_tools_list_options_and_select_one_or_all_v0(root_path_data_for_publication+sname+"/*/"+pkl_file_out.replace(".pkl",".pkl"))
    if not include_systematic_errors : pkl_file_to_read_list,pkl_file_to_read_without_path_obs_list=dt.db_tools_list_options_and_select_one_or_all_v0(root_path_data_for_publication+sname+"/*/"+pkl_file_out.replace(".pkl","_no_sys.pkl"))
    ind_option_lum,option_lum=dt.db_tools_select_an_option_from_menu(["Bolometric luminosity","Blackbody luminosity"])

for pkl_file_to_read in pkl_file_to_read_list :
    print(pkl_file_to_read)
    dt.db_print_message("The pkl file to be read is = "+pkl_file_to_read)

    if ind_persistent_lum == 0 :
#        pkl_file_to_read=pkl_file_to_read.replace(".pkl","_persistent.pkl")
        blackbody_only=False
    else :
        blackbody_only=True
        print("ind_option=",ind_option_lum,option_lum)
        if ind_option_lum == 0 : blackbody_only=False
        if blackbody_only and pkl_file_to_read.find("fa") > 0 :
            dt.db_print_message("This is a fit with the fa model : I am going to cancel the constant to derive the BB flux -> file : "+pkl_file_to_read.replace(".pkl","_with_fx_lx_bb.pkl"))

    list_pha_obj=dt.restore_pickle_objects(pkl_file_to_read)
    list_pha_obj_with_lx=[]
    for i_pha in range(len(list_pha_obj)):
        fx_and_error,lx_and_error=dt.db_compute_fx_lx_from_simpar(list_pha_obj[i_pha].path_pha,list_pha_obj[i_pha].xcm_filename.replace(".xcm","_all.xcm"), num_sim=np.int32(dyt.db_read_yml(yml_file,"num_simpar")), energy_range=np.array(dyt.db_read_yml(yml_file,"energy_range_for_bolometric_flux_luminosity")), distance_kpc=10.*np.float64(dyt.db_read_yml(yml_file,"distance_in_10kpc")), norm_fx=np.float64(dyt.db_read_yml(yml_file,"norm_fx")), norm_lx=np.float64(dyt.db_read_yml(yml_file,"norm_lx")),blackbody_only=blackbody_only,compute_errors=True)
        list_pha_obj[i_pha].fx=fx_and_error
        list_pha_obj[i_pha].lx=lx_and_error
        if not blackbody_only : dt.save_pickle_object(list_pha_obj,pkl_file_to_read.replace(".pkl","_with_fx_lx.pkl"))
        if blackbody_only : dt.save_pickle_object(list_pha_obj,pkl_file_to_read.replace(".pkl","_with_fx_lx_bb.pkl"))
