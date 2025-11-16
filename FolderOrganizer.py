import os, math, random, time

class FolderOrganizer:
    def __init__(self, target_files, folder, log_function) -> None:
        self.target_files = target_files
        self.folder = folder
        
        self.files_count = 0
        self.folders_count = 0
        
        self.moved_files = 0
        self.created_folders = 0
        
        self.errors_count = 0
        
        self.log_function = log_function
        
    def create_folders_path(self):
        dirs = []
        for target in self.target_files:
            path = os.path.join(self.folder, target["dir"])
            dirs.append(path)
            target["path"] = path
        return dirs
    
    def create_folders(self, dir_list   ):
        for dir in dir_list:
            try:
                os.mkdir(dir)
                self.created_folders += 1
            except FileExistsError:
                self.log_function(f"Erro: O diretório '{dir}' já existe!")

            except PermissionError:
                self.log_function(f"Erro: Sem permissão para criar o diretório '{dir}'!")
            except OSError as e:
                self.log_function(f"Erro: Não foi possível criar '{dir}'!\nmotivo: {e}")
              
    def move_file(self, file):
        try:
            extension = file.name.split('.')[-1].lower()

            for target in self.target_files:
                if extension in target["extensions"]:
                    new_path = os.path.join(target["path"], file.name)               

                    if (os.path.exists(new_path)):
                        new_path =  os.path.join(target["path"], f'{self.generate_renamed_prefix()}{file.name}')

                    os.rename(file.path, new_path)
                    
                    self.log_function(f"'{file.name}' foi movido para '{new_path}'" )
                    self.moved_files += 1

                self.files_count += 1
        except WindowsError as e:
            self.log_function(f"Erro windows: {e}")
            print(file)
        except Exception as e:
            self.log_function(f"Erro: {e}")
            self.errors_count += 1
                
    def run(self):
        folders = self.create_folders_path()
        self.create_folders(folders)
        
        try: 
            items = os.scandir(self.folder)
            
            for item in items:
                print(f"item: {item.name}")

                if item.is_file():
                    self.move_file(item)
                elif item.is_dir():
                    self.folders_count += 1              
        except FileNotFoundError as e:
            self.log_function(f"Erro: {e}" )
            self.errors_count += 1
        except OSError as e:
            self.log_function(f"Erro: {e}" )
            self.errors_count += 1
            
        self.log_final_status()

    def generate_renamed_prefix(self):
        current_timestamp = math.trunc(time.time())
        return f'renamed_{current_timestamp * random.randint(2,9)}_'
            
    def log_final_status(self):
        self.log_function("= = = = = = = = = = = = = = = = = = = = = = = = = = =")  
        self.log_function("= = = = = = = = = =   RESUMO    = = = = = = = = = = =")
        self.log_function("= = = = = = = = = = = = = = = = = = = = = = = = = = =")
        self.log_function(f"total de arquivos: {self.files_count}")
        self.log_function(f"total de pastas: {self.folders_count}")
        self.log_function(f"total de arquivos e pastas: {self.files_count + self.folders_count}")
        self.log_function(f"total de arquivos movidos: {self.moved_files}")
        self.log_function(f"total de pastas criadas: {self.created_folders}")        
        self.log_function(f"total de erros: {self.errors_count}")
        self.log_function("= = = = = = = = = = = = = = = = = = = = = = = = = = =") 
        self.log_function("= = = = = = = =    FINALIZADO     = = = = = = = = = =")
        self.log_function("= = = = = = = = = = = = = = = = = = = = = = = = = = =")
        
              