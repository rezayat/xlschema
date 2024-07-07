package ${model.nspace.app};

% if 'Date' in model.types:
import java.util.*;
% endif
import javax.persistence.*;

@Entity
public class ${model.classname} {

    % for definition in model.definitions:
    ${definition}
    % endfor

    public ${model.classname}() {}

    % for method in model.methods:
    ${method}
    % endfor
}
