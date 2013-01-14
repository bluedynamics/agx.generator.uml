import profile
import hierarchy
import datatypedependent
import stereotypes


def register():
    """Register this generator.
    """
    import agx.generator.uml
    from agx.core.config import register_generator
    register_generator(agx.generator.uml)
