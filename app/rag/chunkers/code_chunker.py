import ast

class CodeChunker:

    def chunk(self, code):
        chunks=[]
        for code_file in code:
            file_chunks=self._chunk_file(code_file)
            chunks.extend(file_chunks)
        
        return chunks

    def _chunk_file(self, code_file):
        source=code_file["content"]
        path=code_file["path"]
        chunks=[]
        module_nodes=[]
        try:
            tree=ast.parse(source)
        except SyntaxError:
            return self._fallback_chunk(code_file)
        
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                chunk= self._extract_classes(node, source, path)
                chunks.append(chunk)
            elif isinstance(node, ast.FunctionDef):
                chunk= self._extract_functions(node, source, path)
                chunks.append(chunk)
            else:
                module_nodes.append(node)

        if module_nodes:
            chunk=self._extract_module_code(module_nodes, source, path)
            chunks.append(chunk)
        
        return chunks


    def _extract_classes(self, node, source , path):
        #type(node).__name__
        name= node.name
        content= ast.get_source_segment(source, node)
        chunk= {
            "type":"class",
            "name":name,
            "path":path,
            "content":content,
        }
        return chunk


    def _extract_functions(self, node, source, path):
        name= node.name
        content= ast.get_source_segment(source, node)
        chunk={
            "type":"function",
            "name":name,
            "path":path,
            "content":content,
        }
        return chunk
    
    def _extract_module_code(self, module_nodes, source, path):
        content=""
        for node in module_nodes:
            c= ast.get_source_segment(source, node)
            if c: # if the ast.get_source_segment returns None
                content += c + "\n\n"
        chunk={
            "type":"module",
            "name":None,
            "path":path,
            "content":content,

        }
        return chunk

    def _fallback_chunk(self, code_file ):
        path=code_file["path"]
        content=code_file["content"]
        chunks=[
            {
            "type":"file",
            "name":None,
            "path":path,
            "content":content
            }
        ]
        return chunks