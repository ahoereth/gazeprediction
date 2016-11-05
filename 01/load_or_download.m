function img = load_or_download(image, indir)    
    [imagepath, imagename, imageext] = fileparts(image);
    
    store = true;
    if any(arrayfun(@(f) strcmp(f.name, [imagename imageext]), dir(indir)))
        imagepath = indir;
        store = false;
    end
    
    img = imread([imagepath filesep imagename imageext]);
    
    if store
        imwrite(img, [indir filesep imagename imageext]);
    end
end