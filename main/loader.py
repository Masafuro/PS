import importlib.util
import os
import config  # ドットを消しました

def get_execute_functions(phase_folder):
    funcs = []
    target_dir = os.path.join(config.PROJECT_ROOT, config.SRC_DIR_NAME, phase_folder)
    
    if not os.path.exists(target_dir):
        return funcs

    files = sorted([f for f in os.listdir(target_dir) if f.endswith(config.SCRIPT_EXTENSION)])
    
    for file_name in files:
        file_path = os.path.join(target_dir, file_name)
        module_name = f"{phase_folder}_{file_name[:-len(config.SCRIPT_EXTENSION)]}"
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'execute'):
            funcs.append((file_name, module.execute))
    
    return funcs