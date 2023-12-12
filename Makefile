
build_sim:
	bazel build //ocs_cache_sim:run_cache_sim

refresh:
	#cd ocs_cache_sim && bazel run @hedron_compile_commands//:refresh_all
	bazel run @hedron_compile_commands//:refresh_all
