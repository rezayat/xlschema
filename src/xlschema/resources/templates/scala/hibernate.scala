package ${model.nspace.app}

% if 'Date' in model.types:
import java.util._
% endif
import javax.persistence._
import scala.reflect.BeanProperty

@Entity
class ${model.classname} {

    % for definition in model.definitions:
    ${definition}
    % endfor

    def this() = this (null, null)

    override def toString = "< ${model.classname} " + id + " >"
}
