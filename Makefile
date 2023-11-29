
build_sim:
	unlink run_cache_sim
	bazel build //cache:run_cache_sim
	ln -s ./bazel-bin/cache/run_cache_sim run_cache_sim
