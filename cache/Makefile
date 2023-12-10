
build_sim:
	bazel build //:all
	bazel run @hedron_compile_commands//:refresh_all --compilation_mode=dbg
	unlink run_cache_sim
	ln -s ./bazel-bin/run_cache_sim
